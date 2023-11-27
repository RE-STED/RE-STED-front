import os
import random

def random_choice(a : list):
    
    # 선택한 파일이름이 .DS_Store이면 다시 선택
    while True:
        choice = random.choice(a)
        if choice != '.DS_Store':
            break
    return choice