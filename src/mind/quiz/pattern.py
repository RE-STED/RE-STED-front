# -*- coding: utf-8 -*-
import random
from ..qt6.patternQT import PatternWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsOpacityEffect, QStackedLayout, QPushButton, QSizePolicy


class FindPatterns(PatternWindow):
    def __init__(self):
        super().__init__()
        
        # Qt Setting
        self.set_btn()
        #self.BackgroundGrapicView.setStyleSheet("background-image: url(qt6/img/bgi.jpeg);")
        self.setStyleSheet("background-color: white;")
         # Create a QGraphicsOpacityEffect object
        self.opacity_effect = QGraphicsOpacityEffect(self)
        # Set the opacity level. The value should be between 0 (completely transparent) and 1 (completely opaque).
        self.opacity_effect.setOpacity(0.8)
        # Apply the opacity effect to the button
        self.setGraphicsEffect(self.opacity_effect)
        
        self.Answer0.clicked.connect(self.game); self.Answer1.clicked.connect(self.game); self.Answer2.clicked.connect(self.game)
        self.Answer3.clicked.connect(self.game); self.Answer4.clicked.connect(self.game); self.Answer5.clicked.connect(self.game)
        self.Answer6.clicked.connect(self.game); self.Answer7.clicked.connect(self.game); self.Answer8.clicked.connect(self.game); self.Answer9.clicked.connect(self.game)
        
        self.set_style(self.Answer0); self.set_style(self.Answer1); self.set_style(self.Answer2); self.set_style(self.Answer3); self.set_style(self.Answer4)
        self.set_style(self.Answer5); self.set_style(self.Answer6); self.set_style(self.Answer7); self.set_style(self.Answer8); self.set_style(self.Answer9)
        
        self.HomeButton.clicked.connect(self.close_window)
        self.HomeButton.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 50); font-size: 48pt; color: white; border-radius: 1.5em;} QPushButton:hover { background-color: rgba(0, 0, 0, 100); font-weight: bold; font-size: 50pt;}");

        
        # Game Setting
        self.size = 9
        self.tile = {'heart' : '❤️', 'spade' : '♠️', 'diamond' : '♦️', 'club' : '🍀', 'star' : '⭐️', 'circle' : '🔵'}
        self.color_tile = {'heart' : 'red', 'spade' : 'black', 'diamond' : 'red', 'club' : 'green', 'star' : 'gold', 'circle' : 'blue'}
        self.count = dict.fromkeys(self.tile.keys(), 0)
        self.coordinate = {key: set() for key in self.tile.keys()}
        
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        #1  4 6 9
        self.lon = {1 : [0, 7, 8], 2:[1, 4, 6, 9], 3:[2, 3, 5]}
        
        self.target_tile = random.choice(list(self.tile.keys()))
        
        # QusetionText의 글자 크기를 조절하려면
        self.QuestionText.setStyleSheet("font-size: 40pt;")
        self.QuestionText.setText(f"{self.tile[self.target_tile]}를 모두 클릭하고 숨겨진 숫자를 찾아보세요.")
        
        self.cor_answer = set([])

    
    def make_random_board(self, level):
        
        self.target_num = random.choice(self.lon[level])
        self.make_number(self.target_num)
        
        # 가능한 문양들
        symbols = [key for key in self.tile.keys() if key != self.target_tile]
        #print(self.target_num)
        
        # 각 셀에 대해 랜덤한 문양 선택
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != '':
                    continue
                random_tile = random.choice(symbols)
                self.add_board(i, j, random_tile)
        self.make_qt_board()

    def game(self):
        btn = self.sender()
        num_answer = int(btn.text())
        self.check_answer(num_answer)
        
        
    def add_cordinate(self):
        btn = self.sender()
        index = self.GameBoard.indexOf(btn)
        y, x, _, _ = self.GameBoard.getItemPosition(index)
        if btn.isFlat():
            self.cor_answer.discard((y, x))
            btn.setStyleSheet("QPushButton { background-color: white; font-size: 30pt; color: black; border-radius: 1.2em;} QPushButton:hover { font-weight: bold; }");
            

        else:
            self.cor_answer.add((y, x))
            btn.setStyleSheet("QPushButton { background-color: black; font-size: 30pt; color: white; border-radius: 1.2em;} QPushButton:hover { font-weight: bold; }")


        
    def add_board(self, i, j, tile_name):
        self.board[i][j] = self.tile[tile_name]
        self.count[tile_name] += 1
        self.coordinate[tile_name].add((i, j))
        
    def make_number(self, n):

        if n == 0 : 
            for i in range(1,8):
                if i == 1 or i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                else:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
        elif n == 1 :
            for i in range(1,8):
                self.add_board(i, 4, self.target_tile)
                if i == 2:
                    self.add_board(i, 3, self.target_tile)
                elif i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                        
        elif n == 2 :
            for i in range(1,8):
                if i == 1:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 2:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                elif i == 3:
                    self.add_board(i, 6, self.target_tile)
                elif i == 4:
                    self.add_board(i, 5, self.target_tile)
                elif i == 5:
                    self.add_board(i, 4, self.target_tile)    
                elif i == 6:
                    self.add_board(i, 3, self.target_tile)
                elif i == 7:
                    for j in range(2, 7):
                        self.add_board(i, j, self.target_tile)
                        
        elif n == 3 :
            for i in range(1, 8):
                if i == 1:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 2:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                elif i == 3:
                    self.add_board(i, 6, self.target_tile)
                elif i == 4:
                    for j in range(4, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 5:
                    self.add_board(i, 6, self.target_tile)
                elif i == 6:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                elif i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                        
        elif n == 4 :
            for i in range(1, 8):
                if i == 1:
                    self.add_board(i, 5, self.target_tile)
                elif i == 2:
                    self.add_board(i, 4, self.target_tile)
                    self.add_board(i, 5, self.target_tile)
                elif i == 3:
                    self.add_board(i, 3, self.target_tile)
                    self.add_board(i, 5, self.target_tile)
                elif i == 4:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 5, self.target_tile)
                elif i == 5:
                    for j in range(2, 7):
                        self.add_board(i, j, self.target_tile)
                elif i == 6:
                    self.add_board(i, 5, self.target_tile)
                elif i == 7:
                    self.add_board(i, 5, self.target_tile)
                    
        elif n == 5 :
            for i in range(1, 8):
                if i == 1:
                    for j in range(2, 7):
                        self.add_board(i, j, self.target_tile)
                elif i == 2 or i == 3:
                    self.add_board(i, 2, self.target_tile)
                elif i == 4:
                    self.add_board(i, 3, self.target_tile)
                    self.add_board(i, 4, self.target_tile)
                    self.add_board(i, 5, self.target_tile)
                elif i == 5 or i == 6:
                    self.add_board(i, 6, self.target_tile)
                elif i == 7:
                    for j in range(2, 6):
                        self.add_board(i, j, self.target_tile)
                        
        elif n == 6 :
            for i in range(1, 8):
                if i == 1 or i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 2 or i == 3:
                    self.add_board(i, 2, self.target_tile)
                elif i == 4:
                    for j in range(2, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 5 or i == 6:
                    self.add_board(i, 6, self.target_tile)
                    self.add_board(i, 2, self.target_tile)
                    
        elif n == 7 :
            for i in range(1,8):
                if i == 1:
                    for j in range(2, 7):
                        self.add_board(i, j, self.target_tile)
                self.add_board(i, 6, self.target_tile)
        
        elif n == 8:
            for i in range(1,8):
                if i == 1 or i == 4 or i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 2 or i == 3:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                elif i == 5 or i == 6:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                    
        elif n == 9:
            for i in range(1, 8):
                if i == 1 or i == 7:
                    for j in range(3, 6):
                        self.add_board(i, j, self.target_tile)
                elif i == 2 or i == 3:
                    self.add_board(i, 2, self.target_tile)
                    self.add_board(i, 6, self.target_tile)
                elif i == 4:
                    for j in range(3, 7):
                        self.add_board(i, j, self.target_tile)
                elif i == 5 or i == 6:
                    self.add_board(i, 6, self.target_tile)
                
    def print_board(self):
        print(' ', end=' ')
        for i in range(self.size):
            print(i, end=' ')
        print()
        for i, row in enumerate(self.board):
            print(i, ' '.join(row))
            
        
    def check_answer(self, num_answer):

        '''
        self.coordinate와 self.cor_answer[self.target_tile]을 비교해서 좌표 구성이 같은지 확인
        '''
        # print(self.cor_answer)
        # print(self.coordinate[self.target_tile])
        if self.cor_answer == self.coordinate[self.target_tile] and num_answer == self.target_num:
            print("정답!")
            self.show_ending_message(True)
            self.parent.btnWidget.show()
            self.parent.layout.removeWidget(self)
            
        else:
            # if self.cor_answer != self.coordinate[self.target_tile]:
            #     print("빠진 문자가 있는지 확인해주세요.")
            # if num_answer != self.target_num:
            #     print("숨겨진 숫자를 다시 확인해주세요.")
            self.show_ending_message(False)


        
    def make_qt_board(self):
        for i in range(self.size):
            for j in range(self.size):
                button = self.GameBoard.itemAtPosition(i, j).widget()
                button.setFixedSize(70, 70)
                #button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setText(self.board[i][j])
                
                button.setStyleSheet("QPushButton { background-color: white; font-size: 30pt; color: black; border-radius: 1.5em;} QPushButton:hover { font-weight: bold; }");
                
                button.clicked.connect(self.add_cordinate)
