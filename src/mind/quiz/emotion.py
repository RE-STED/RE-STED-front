# -*- coding: utf-8 -*-

import os
import time
import cv2
import random
from tqdm import tqdm
import sys
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

from ..utils.util import random_choice
from ..utils.GAN.StarGAN import *
from ..qt6.emotionQT import EmotionBoard

class EmotionWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # PyQt6
        self.resize(800, 600)
        self.stack = EmotionBoard()
        self.setCentralWidget(self.stack)
        self.stack.widget(0).findChild(QPushButton, "SelectCeleb").clicked.connect(self.Start)
        self.stack.widget(0).findChild(QPushButton, "SelectFamily").clicked.connect(self.Start)
        
        self.stack.widget(2).findChild(QPushButton, "SadBtn_2").clicked.connect(self.push_answer)
        self.stack.widget(2).findChild(QPushButton, "AngryBtn_2").clicked.connect(self.push_answer)
        self.stack.widget(2).findChild(QPushButton, "HappyBtn_2").clicked.connect(self.push_answer)
        self.stack.widget(2).findChild(QPushButton, "NeutralBth_2").clicked.connect(self.push_answer)
        self.stack.widget(2).findChild(QPushButton, "FearfulBtn_2").clicked.connect(self.push_answer)
        self.stack.widget(2).findChild(QPushButton, "SurpriseBtn_2").clicked.connect(self.push_answer)
        
        self.stack.widget(2).findChild(QPushButton, "InputAnswer").clicked.connect(self.Check)
        
        self.stack.widget(3).findChild(QPushButton, "SadBtn").clicked.connect(self.push_answer)
        self.stack.widget(3).findChild(QPushButton, "AngryBtn").clicked.connect(self.push_answer)
        self.stack.widget(3).findChild(QPushButton, "HappyBtn").clicked.connect(self.push_answer)
        self.stack.widget(3).findChild(QPushButton, "NeutralBth").clicked.connect(self.push_answer)
        self.stack.widget(3).findChild(QPushButton, "FearfulBtn").clicked.connect(self.push_answer)
        self.stack.widget(3).findChild(QPushButton, "SurpriseBtn").clicked.connect(self.push_answer)
        
        
        self.model = StarGAN
        
        self.Gallery = "Gallery"
        
        self.label = ['angry', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
        self.answer = None
        
    def Start(self):
        category = 1 if self.sender().text() == '가족' else 2
        
        self.img_path, self.mode = self.get_who(str(category))
        print(self.img_path)
        if self.mode == 'origin_person':
            img_label = self.stack.widget(1).findChild(QLabel, "ImgForOne")
        elif self.mode == 'group':
            img_label = self.stack.widget(1).findChild(QLabel, "ImgForGroup")
        pixmap = QPixmap(self.img_path).scaled(img_label.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        img_label.setPixmap(pixmap)
        
        self.stack.widget(1).findChild(QLabel, "name").setText(self.who)
        self.stack.setCurrentIndex(1)
        
        time.sleep(3)
        
        self.Quiz()
        
    
    def get_who(self, category) -> str :
        if category == "2":
            mode = random.choice(['origin_person', 'group'])
            category2 = 'group' if mode == 'group' else 'solo'
            
            celeb_list = os.listdir(f"{self.Gallery}/celeb/{category2}/")
            name = random_choice(celeb_list)
            
            self.img_dir = f'{self.Gallery}/celeb/{category2}/{name}/'
            
        
        elif category == '1':
            mode = 'origin_person'
            family_list = os.listdir(f'{self.Gallery}/family/')
            name = random_choice(family_list)
        
            self.img_dir = f'{self.Gallery}/family/{name}/'
        
        # img_dir에서 랜덤으로 사진 하나 골라오기
        img_list = os.listdir(self.img_dir)
        img_name = random_choice(img_list)
        
        self.who = self.img_dir.split('/')[-2]
        print(f'선택된 인물은 {self.who} 입니다.')
        return self.img_dir + img_name, mode
    
    def Quiz(self):

        
        # 메시지 박스 생성
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("이미지를 변환하는 중입니다...")
        msg.setWindowTitle("진행 중")
        #msg.setStandardButtons(QMessageBox.StandardButton.NoButton)
        
        # 메시지 박스 띄우기
        retval = msg.exec()
        
        facial_dict = self.model().ConvertFace(img_path = self.img_path, 
                                               trans_mode = self.mode)
        
        msg.close()
        
        if self.mode == 'origin_person':
            who = list(facial_dict.keys())[0]
            
            img_collection = facial_dict[who]
            self.target = random.choice(list(img_collection.keys()))
            
            img = img_collection[self.target].numpy().transpose(1,2,0)
            cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            img_label = self.stack.widget(3).findChild(QLabel, "Person")
            w, h = img_label.width(), img_label.height()
            img = QPixmap(self.np2Qimg(img)).scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            img_label.setPixmap(img)
            
            self.stack.setCurrentIndex(3)
            
                

                
        elif self.mode == 'group':
            self.answer = []
            who = list(facial_dict.keys())[0]
            
            img_collection = facial_dict[who]
            self.target = facial_dict['answer']
            img = img_collection.numpy().transpose(1,2,0)
            cv2.imshow('img', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            img_label = self.stack.widget(2).findChild(QLabel, "People")
            w, h = img_label.width(), img_label.height()
            img = self.np2Qimg(img).scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            img_label.setPixmap(img)
            
            self.stack.setCurrentIndex(2)
            
            
                
    def push_answer(self):
        btn_label = ['화남', '두려움', '행복함', '무표정', '슬픔', '놀람']
        if self.mode == 'origin_person':
            self.answer = btn_label.index(self.sender().text())
            AnswerMsg = QMessageBox()
            AnswerMsg.setIcon(QMessageBox.Icon.Information)
            if self.target == self.label[self.answer]:
                AnswerMsg.setText("정답입니다!")
                AnswerMsg.setWindowTitle("정답")
                AnswerMsg.buttonClicked.connect(self.End)
                AnswerMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
                AnswerMsg.exec()
            else:
                AnswerMsg.setText("틀렸습니다! 다시 해보세요")
                AnswerMsg.setWindowTitle("오답")
                AnswerMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
                AnswerMsg.exec()
        
        elif self.mode == 'group':
            if self.sender().isFlat() == False:
                self.sender().setFlat(True)
                self.answer.append(btn_label.index(self.sender().text()))
            else:
                self.answer.remove(btn_label.index(self.sender().text()))
                self.sender().setFlat(False)
            
            
    def Check(self):
        self.answer = sorted(self.answer)
        self.target = sorted(self.target)
        
        # answer와 target의 구성이 같으면 정답
        if self.answer == self.target:
            AnswerMsg = QMessageBox()
            AnswerMsg.setIcon(QMessageBox.Icon.Information)
            AnswerMsg.setText("정답입니다!")
            AnswerMsg.setWindowTitle("정답")
            AnswerMsg.buttonClicked.connect(self.End)
            AnswerMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
            AnswerMsg.exec()
        else:
            AnswerMsg = QMessageBox()
            AnswerMsg.setIcon(QMessageBox.Icon.Information)
            AnswerMsg.setText("틀렸습니다! 다시 해보세요")
            AnswerMsg.setWindowTitle("오답")
            AnswerMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
            AnswerMsg.exec()
        
    def End(self):
        # 창 아예 닫기
        self.close()
        
    def np2Qimg(self, input):
        print(input.shape)
        height, width, channel = input.shape
        input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
        bytesPerLine = 3 * width
        qImg = QImage(input.tobytes(), width, height, bytesPerLine, QImage.Format.Format_RGB888)
    
        pixmap = QPixmap(qImg)
        
        return pixmap
        