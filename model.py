# Wordle Model
import string
import pandas as pd
import math
import random
import enum
import pygame
import time
import sqlite3

conn = sqlite3.connect('wordleDB.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#attempt at enum
class Guess(enum.Enum):
   NOT_GUESSED = 1
   NOT_IN_WORD = 2
   NOT_IN_PLACE = 3
   PERFECT = 4

class Wordle_Model():
    def __init__(self, db = "wordleDB.db") -> None:
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.current_word = self.get_wordle_word() # the word the player is trying to guess currently
        print("word is " + self.current_word)
        self.guesses = 0
        self.game_over = False
        self.letter_dic = {}
        self.word_progress = [Guess.NOT_GUESSED] * 5
        self.past_words = []
        self.populate_letter_dic()
    
    def populate_letter_dic(self):
        letters = string.ascii_uppercase # [A-Z]
        default = Guess.NOT_GUESSED

        for letter in letters:
            self.letter_dic[letter] = default
    
    def view_model_state(self):
        print("letter dic: ", self.letter_dic)
        print("current word: ", self.current_word)
        print("num gueses: ",self.guesses)
        print("game over? ", self.game_over)
    
    def reset_game_state(self):
        '''Resets the game state'''
        self.populate_letter_dic()
        self.current_word = self.get_wordle_word()
        self.guesses = 0
        self.game_over = False

    def get_guess_number(self):
        return self.guesses

    def get_letter_dic(self):
        return self.letter_dic
    
    def check_valid_guess(self, guess):
        '''This method queries the database to validate a user guess. It 
            returns True if the user inputted a real word, and False otherwise
            After confirming a valid guess, calls are made to update game state'''

        if self.cur.execute("SELECT 1 FROM ALL_WORDS WHERE word =:guess", {"guess":guess}).fetchone():
            self.update_letter_dic(guess)
            self.increment_guesses()
            return True

        return False
    
    def compare_single_guess(self, guess):
        #guess is a list
        res = [Guess.NOT_GUESSED] * 5
        for i in range(5):
            if guess[i] == self.current_word[i]:
                res[i] = Guess.PERFECT
            elif guess[i] in self.current_word:
                res[i] = Guess.NOT_IN_PLACE
            else:
                res[i] = Guess.NOT_IN_WORD
        return res

    
    def is_valid_guess(self, guess):
        '''This method returns True if the guess is valid,
            otherwise False'''
        if (guess.isalnum() and len(guess) == 5 and guess in self.all_words):
            self.update_letter_dic(guess)
            self.increment_guesses()
            return True

        return False
    def get_wordle_word(self):
        '''This method returns a valid word '''
        # selecting a random wid from wordle_words table
        self.cur.execute("SELECT * FROM WORDLE_WORDS ORDER BY RANDOM() LIMIT 1;")
        num = self.cur.fetchone()[0]
        # looking about the actual word by wid in all words table
        self.cur.execute("SELECT word FROM ALL_WORDS WHERE wid =:key", {"key":num})
        word = self.cur.fetchone()[0]
        print(word)
        return word
        
    def increment_guesses(self):
        self.guesses +=1

    def check_guess(self, user_guess):
        '''This method checks if a user correctly guessed
            the word. Returns True if so, False otherwise.'''
        # the user correctly guessed, good job!
        if user_guess == self.current_word: 
            print('You Win')
            self.game_over = True
            self.past_words.append(user_guess)
            return True
        
        return False
    
    def update_letter_dic(self, user_guess):
        '''This method will update the letter_dictionary
            based on user guesses, and maintain game state.'''
        "EARTH"
        "AISLE"
        for i in range(5):
            if user_guess[i] in self.current_word:
                if user_guess[i] == self.current_word[i]:
                    #color it green
                    self.letter_dic[user_guess[i]] = Guess.PERFECT
                else:
                    #color it orange, its still in the word...
                    self.letter_dic[user_guess[i]] = Guess.NOT_IN_PLACE
            else:
                #color it black
                self.letter_dic[user_guess[i]] = Guess.NOT_IN_WORD
   

def main():
    model_test = Wordle_Model([], [])


    model_test.update_letter_dic("AISLE")
    model_test.increment_guesses()
    model_test.view_model_state()

    model_test.reset_game_state()
    model_test.view_model_state()


#main()










    




        
