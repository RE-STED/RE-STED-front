# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import *
import sys

from quiz.pattern import *
from quiz.object import *
from utils.GAN.StarGAN import *
from quiz.emotion import *


class CognitiveTest():
    def __init__(self):
        
        self.GameList = ['pattern', 'object', 'emotion']
        
        #self.app = QApplication(sys.argv)
        
    def PatternGame(self, level):
        self.app = QApplication(sys.argv)
        find_pattern = FindPatterns()
        
        find_pattern.make_random_board(level)
        find_pattern.show()

        self.app.exec()

        
    def ObjectGame(self):
        self.app = QApplication(sys.argv)
        object_quiz = WebcamWidget()#ObjectQuiz()

        object_quiz.show()
        #object_quiz.start()

        self.app.exec()
        
    def EmotionGame(self):
        self.app = QApplication(sys.argv)
        emotion = EmotionWindow()
        emotion.show()
        
        self.app.exec()
        
    def StartGame(self, game, level = 1):
        
        if game == 'pattern':
            self.PatternGame(level)
        elif game == 'object':
            self.ObjectGame()
        elif game == 'emotion':
            self.EmotionGame()
        else:
            print("Wrong Game")


# 'pattern', 'object', 'emotion'
def main(game = 'object', level = 1):

    T = CognitiveTest()
    T.StartGame(game, level)
    
if __name__ == '__main__':
    main('object', 3)