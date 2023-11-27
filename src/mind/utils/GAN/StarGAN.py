# -*- coding: utf-8 -*-

import os
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.utils import save_image
from torchvision import transforms as T
import cv2
import numpy as np
import random
from tqdm import tqdm
from PIL import Image
from collections import OrderedDict

from ..GAN.face_detection import detection_and_resize_original, get_face_mesh
from ..GAN.model import Generator, Discriminator

class StarGAN:
    """Solver for training and testing StarGAN."""

    def __init__(self):

        # Model configurations.
        self.c_dim = 6
        self.image_size = 128
        self.g_conv_dim = 64
        self.d_conv_dim = 64
        self.g_repeat_num = 6
        self.d_repeat_num = 6

        # Test configurations.
        self.test_iters = 330000

        # Miscellaneous.
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #print("Device: ", self.device)

        # Directories.
        self.model_save_dir = "model/gan/"

        # Build the model and tensorboard.
        self.g_lr = 0.0001
        self.d_lr = 0.0001
        self.beta1 = 0.5
        self.beta2 = 0.999
        
        self.build_model()
            
        self.label = ['angry', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

    def build_model(self):
        """Create a generator and a discriminator."""

        self.G = Generator(self.g_conv_dim, self.c_dim, self.g_repeat_num)
        self.D = Discriminator(self.image_size, self.d_conv_dim, self.c_dim, self.d_repeat_num) 
        
        self.g_optimizer = torch.optim.Adam(self.G.parameters(), self.g_lr, [self.beta1, self.beta2])
        self.d_optimizer = torch.optim.Adam(self.D.parameters(), self.d_lr, [self.beta1, self.beta2])
        
        # self.print_network(self.G, 'G')
        # self.print_network(self.D, 'D')
            
        self.G.to(self.device)
        self.D.to(self.device)


    def print_network(self, model, name):
        """Print out the network information."""
        num_params = 0
        for p in model.parameters():
            num_params += p.numel()
        print(model)
        print(name)
        print("The number of parameters: {}".format(num_params))

    def restore_model(self, resume_iters):
        """Restore the trained generator and discriminator."""
        #print('Loading the trained models from step {}...'.format(resume_iters))
        G_path = os.path.join(self.model_save_dir, '{}-G.ckpt'.format(resume_iters))
        D_path = os.path.join(self.model_save_dir, '{}-D.ckpt'.format(resume_iters))
        #self.G.load_state_dict(torch.load(G_path, map_location=lambda storage, loc: storage))
        #self.D.load_state_dict(torch.load(D_path, map_location=lambda storage, loc: storage))
        saved_checkpoint_G = torch.load(G_path, map_location= self.device)
        saved_checkpoint_D = torch.load(D_path, map_location= self.device)

        self.G.load_state_dict(saved_checkpoint_G, strict = False)
        self.D.load_state_dict(saved_checkpoint_D, strict = False)
        

    def denorm(self, x):
        """Convert the range from [-1, 1] to [0, 1]."""
        out = (x + 1) / 2
        return out.clamp_(0, 1)

    def label2onehot(self, labels, dim):
        """Convert label indices to one-hot vectors."""
        batch_size = labels.size(0)
        out = torch.zeros(batch_size, dim)
        out[np.arange(batch_size), labels.long()] = 1
        return out

    def create_labels(self, c_org, c_dim=5):
        """Generate target domain labels for debugging and testing."""
        # Get hair color indices.
        c_trg_list = []
        for i in range(c_dim):
            
            c_trg = self.label2onehot(torch.ones(c_org.size(0))*i, c_dim)

            c_trg_list.append(c_trg.to(self.device))
        return c_trg_list
    
    def ConvertFace(self, img_path, trans_mode = 'origin_person'):
        """Translate images using StarGAN trained on a single dataset."""
        # Load the trained generator.
        self.restore_model(self.test_iters)
        
        if trans_mode == 'group':

            path = img_path
            
            Person_result = {}
            
            img_file = cv2.imread(path)
            name = path.split('/')[-2] 
            print(f'{name} 표정을 변환합니다.')
            
            img_list = detection_and_resize_original(img_file)

            totensor = T.ToTensor()
            norm = T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
            
            img_file = cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB)
            #img_file = cv2.cvtColor(img_file, cv2.COLOR_BGR2RGB)
            original = totensor(img_file)
            original = norm(original)

            print("Original size : {}".format(original.shape))
            
            answer = []
            
            for k, image in enumerate(img_list):
                if k == 0:
                    continue
                img, (x, y, w, h) = image
                
                #print(img.size, x, y, w, h)
                #img.show()
                image_size = img.size[0]
                
                transform = []
                
                transform.append(T.CenterCrop(image_size))
                transform.append(T.ToTensor())
                transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
                transform = T.Compose(transform)

                x_real = transform(img)
                
                x_real = x_real.view(1, 3, image_size, image_size)
                c_org = torch.Tensor([3])
                #print("Size of x_real is {}".format(x_real.size()))
                with torch.no_grad():
                    x_real = x_real.to(self.device)
                    c_trg_list = self.create_labels(c_org, self.c_dim)

                    # Translate images.
                    x_fake_list = [x_real]
                    for c_trg in c_trg_list:
                        x_fake_list.append(self.G(x_real, c_trg))
                    
                    rand_idx = random.randint(1, self.c_dim)
                    answer.append(rand_idx-1)
                    tranlate_img = x_fake_list[rand_idx].data.cpu().squeeze(0) 
                    #print("Size of translate_img : {}".format(tranlate_img.shape))
                    for j in range(3):
                        for i in range(y, y+h):
                            original[j][i][x:x+w] = tranlate_img[j][i-y]
                    print(f'Translate Face expression {k}')

            Person_result[name] = self.denorm(original.data.cpu())
            Person_result['answer'] = answer
            return Person_result
        
        ###########################################################################################################
        elif trans_mode == 'origin_person':
            
            
            Person_result = {}
            
            path = img_path
            img_file = cv2.imread(path)
            name = path.split('/')[-2]
            print(f'{name} 표정을 변환합니다.')
            img_list = detection_and_resize_original(img_file)
            
            #img_list[1][0].show()
            #img_list[0]
            totensor = T.ToTensor()
            norm = T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))
            
            img_file = cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB)

            original = totensor(img_file)
            original = norm(original)

            img, (x, y, w, h) = img_list[1]
                
            #print(img.size)

            image_size = img.size[0]
            
            transform = []
            
            #transform.append(T.CenterCrop(image_size))
            transform.append(T.ToTensor())
            transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
            transform = T.Compose(transform)
            
            x_real = transform(img)
            tf = T.ToPILImage()
            img_np = tf(x_real)
            x_real = x_real.view(1, 3, image_size, image_size)
            
            c_org = torch.Tensor([3])
            #print("Size of x_real is {}".format(x_real.size()))

            with torch.no_grad():
                x_real = x_real.to(self.device)
                c_trg_list = self.create_labels(c_org, self.c_dim)

                # Translate images.
                x_fake_list = [x_real]
                x_origin_list = [original]
                x_mesh_list = [original]

                for c_trg in c_trg_list:
                    x_fake_list.append(self.G(x_real, c_trg))
                    x_origin_list.append(torch.tensor(original))
                    x_mesh_list.append(torch.tensor(original))

                result = {}
                for i, fake in enumerate(x_fake_list):
                    
                    tranlate_img = fake.data.cpu().squeeze(0)

                    #print("Size of translate_img : {}".format(tranlate_img.shape))
                    
                    from torchvision.transforms.functional import to_pil_image

                    for j in range(3):
                        for k in range(y, y+h):
                            x_origin_list[i][j][k][x:x+w] = tranlate_img[j][k-y]
                    
                    face_dict, mesh_img = get_face_mesh(to_pil_image(0.5 * x_origin_list[i] +0.5))
                    
                    tf= T.Compose([T.ToTensor(), T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))])
                    mesh_tensor = tf(mesh_img)
                    
                    for j in range(3):
                        for y1, x_list in face_dict.items():
                            if len(x_list) == 1:
                                continue
                            x1, x2 = x_list
                            x_mesh_list[i][j][y1][x1:x2] = mesh_tensor[j][y1][x1:x2]

                    if i == 0:
                        continue
                    else:
                        result[self.label[i-1]] = self.denorm(x_mesh_list[i].data.cpu())
                        print(f'Translate Face expression {self.label[i-1]}')
                        
                x_concat = torch.cat(x_mesh_list, dim=2)
                #result['total'] = self.denorm(x_concat.data.cpu())
                
            Person_result[name] = result
            return Person_result
        
class EmotionRecognition:
    def __init__(self) -> None:
        
        self.model = StarGAN
        
        self.img_dir = "Gallery"
        
        self.label = ['angry', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
    
    def get_who(self) -> str :
        print("--------------------------------------------")
        category1 = input(" 1. 가족\n 2. 연예인\n\n 번호를 입력하세요 :")
        
        if category1 == "2":
            mode = random.choice(['origin_person', 'group'])
            category2 = 'group' if mode == 'group' else 'solo'
            
            celeb_list = os.listdir(f"{self.img_dir}/celeb/{category2}/")
            if '.DS_Store' in celeb_list:
                celeb_list.remove('.DS_Store')
            name = random.choice(celeb_list)
            
            self.img_dir = f'{self.img_dir}/celeb/{category2}/{name}/'
            
        
        elif category1 == '1':
            mode = 'origin_person'
            family_list = os.listdir(f'{self.img_dir}/family/')
            if '.DS_Store' in family_list:
                family_list.remove('.DS_Store')
            name = random.choice(family_list)
        
            self.img_dir = f'{self.img_dir}/family/{name}/'
            
        else:
            print("Wrong Number\n")
            return self.get_who()
        
        print('\n 설정된 인물들 중 한명을 고르는중 ...\n')
        time.sleep(1)
        
        # img_dir에서 랜덤으로 사진 하나 골라오기
        img_list = os.listdir(self.img_dir)
        img_name = random.choice(img_list)
        
        real_name = self.img_dir.split('/')[-2]
        print(f'선택된 인물은 {real_name} 입니다.')
        return self.img_dir + img_name, mode
    
    def start(self):
        img_path, mode = self.get_who()
        
        print('이미지를 변환하는 중입니다...')
        
        facial_dict = self.model().ConvertFace(img_path = img_path, 
                                               trans_mode = mode)
        
        print('이미지 변환 완료!\n')
        
        if mode == 'origin_person':
            who = list(facial_dict.keys())[0]
            
            img_collection = facial_dict[who]
            target = random.choice(list(img_collection.keys()))
            
            img = img_collection[target].numpy().transpose(1,2,0)
            
            cv2.imshow('Facial', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            cv2.waitKey(0)
            for i, emo in enumerate(self.label):
                print(f' {i+1}. {emo}')
            answer = input(f'\n{who}는 어떤 표정을 짓고 있나요? 번호를 입력하세요 : ')
            
            if target == self.label[int(answer)-1]:
                print('정답입니다!')
            else:
                print('오답입니다!')

                
        elif mode == 'group':
            who = list(facial_dict.keys())[0]
            
            img_collection = facial_dict[who]
            img = facial_dict['total'].numpy().transpose(1,2,0)
            cv2.imshow('Facial', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            cv2.waitKey(0)

            for i, emo in enumerate(self.label):
                print(f' {i+1}. {emo}')
            
            answer_list = map(int, input('사진에 보이는 감정들을 모두 말해주세요. (ex. 1, 2, 3)').split(','))
            for answer in answer_list:
                if answer in facial_dict['answer']:
                    print(f'{self.label[answer-1]} :  정답입니다!')
                else:
                    print(f'{self.label[answer-1]} :  오답입니다!')

        cv2.destroyAllWindows() 
                