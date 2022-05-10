# Wordle View

from cgitb import text
from curses.panel import bottom_panel
import random
from imp import PY_CODERESOURCE
from pandas import date_range
import time

from model import Guess, Wordle_Model
import pygame
import string
import collections

# Load and initalize Pygame
pygame.init()
window_size = [1255, 1255]

# Clock
clock = pygame.time.Clock()

class Wordle_View():
    def __init__(self, model) -> None:
        self.model = model
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wordle")
        #colors
        self.black = (0, 0, 0)
        self.gray = (127, 127, 127)
        self.white = (255, 255, 255)
        self.light_gray = (131,139,139)
        self.dark_gray = (51,51,51)
        self.green = (154,205,50)
        self.gold = (255,185,15)
        # font
        self.font = pygame.font.Font(None, 40)
        self.play_button = pygame.Rect(950,100,240,75)
        self.buttton_object = self.font.render("Play Again?", True, self.dark_gray)
        self.button_text_rect = self.buttton_object.get_rect(center = self.play_button.center)
        self.color_dic = {Guess.NOT_GUESSED:self.gray,
         Guess.NOT_IN_PLACE:self.gold,
         Guess.PERFECT:self.green,
          Guess.NOT_IN_WORD:self.dark_gray}
        self.text_letters = []
        self.rect_dict = {}
        self.grid_box_locations = [[() for col  in range(5)] for row in range(6)]
        self.grid_letter_locations = [[() for col  in range(5)] for row in range(6)]
        self.letter_stack = collections.deque()
        self.guess = []
        # dimensions
        self.WIDTH = 75
        self.HEIGHT = 75
        self.MARGIN = 10
        self.KEY_WIDTH = 50
        self.KEY_HEIGHT = 50
        self.TOP_ROW = 10
        self.MIDDLE_ROW = 9
        self.BOTTOM_ROW = 7

        self.done = False
        self.cur_row = 0
        self.cur_col = 0
        self.letters = ["Q", "W", "E", "R", "T", "Y", "U", "I",
         "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L",
          "Z", "X", "C", "V", "B", "N", "M"]

    def validate_input_word(self):
        '''This method sends off the user input to the model to check 
            for validity. It returns a boolean True if so, and 
            False otherwise'''
        s = "".join(self.guess)
        return self.model.check_valid_guess(s)
    
    def check_for_win(self):
        '''This method asks the model if user input matches the 
            correct word'''
        s = "".join(self.guess)
        return self.model.check_guess(s)

    def request_guess_count(self):
        '''This method asks the model for the current user guess'''
        return self.model.get_guess_number()
    

    def request_game_state(self):
        '''This method returns a request for game state from the 
            model. The model returns its letter dictionary'''
        return self.model.get_letter_dic()
    
    def new_game(self):
        '''This method tells the model to reset itself to new state,
            and resets the user interface.'''
        self.reset_board()
        self.model.reset_game_state()
        
    def reset_board(self):
        '''This method is called to reset the user interface back
            to an empty state so a new round can begin.'''
        self.guess = []
        self.cur_col = 0
        self.cur_row = 0
        self.reset_keyboard()
        self.reset_grid()
        self.hide_reveal()
        self.hide_play_button()
        pygame.display.update()
        clock.tick(50)


    def initial_setup(self):
        '''This method draws the inital user interface and 
            stores positional information so objects can be updated
            and redrawn with ease during runtime.'''
        for row in range(6):
            for col in range(5):
                # Drawing the word grid where guesses will display
                r = pygame.draw.rect(self.screen, self.dark_gray,
                [420 + (self.MARGIN + self.WIDTH) * col + self.MARGIN,
                              (self.MARGIN + self.HEIGHT) * row +self.MARGIN,
                              self.WIDTH,
                              self.HEIGHT])
                x = 420 + (self.MARGIN + self.WIDTH) * col + self.MARGIN
                y = (self.MARGIN + self.HEIGHT) * row +self.MARGIN
                # These matricies store coordinates so we can draw over boxes seamlessly
                self.grid_box_locations[row][col] = (x,y)
                self.grid_letter_locations[row][col] = r.center
        letter_count = 0
        for i in range(len(self.letters)):
            l = self.font.render(self.letters[i], True, self.white)
            self.text_letters.append(l)
        for letter in range(self.TOP_ROW):
            x = (332 + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN)
            y = 550
            self.rect_dict[self.letters[letter_count]] = (x,y)
            r = pygame.draw.rect(self.screen,self.light_gray, [332 + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN, 550, self.KEY_WIDTH, self.KEY_HEIGHT])
            text_rect = self.text_letters[letter_count].get_rect(center = r.center)
            self.screen.blit(self.text_letters[letter_count], text_rect)
            letter_count +=1
        
        for letter in range(self.MIDDLE_ROW):
            x = (332 + self.KEY_HEIGHT//2) + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN
            y = 550 + self.MARGIN + self.KEY_HEIGHT
            self.rect_dict[self.letters[letter_count]] = (x,y)
            r = pygame.draw.rect(self.screen,self.light_gray, [(332 + self.KEY_HEIGHT//2) + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN, 550 + self.MARGIN + self.KEY_HEIGHT, self.KEY_WIDTH, self.KEY_HEIGHT])
            text_rect = self.text_letters[letter_count].get_rect(center = r.center)
            self.screen.blit(self.text_letters[letter_count], text_rect)
            letter_count +=1
        for letter in range(self.BOTTOM_ROW):
            x = (self.MARGIN + 332 + 1.5*(self.KEY_HEIGHT)) + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN
            y =  550 + 2*(self.MARGIN + self.KEY_HEIGHT)
            self.rect_dict[self.letters[letter_count]] = (x,y)
            r = pygame.draw.rect(self.screen,self.light_gray, [(self.MARGIN + 332 + 1.5*(self.KEY_HEIGHT)) + letter*(self.MARGIN + self.KEY_WIDTH) + self.MARGIN, 550 + 2*(self.MARGIN + self.KEY_HEIGHT), self.KEY_WIDTH, self.KEY_HEIGHT])
            text_rect = self.text_letters[letter_count].get_rect(center = r.center)
            self.screen.blit(self.text_letters[letter_count], text_rect)
            letter_count +=1
    
    def run(self):
        '''This is the main loop of the game'''
        last = "None"
        while not self.done:
            if self.request_guess_count() > 5 or self.model.game_over:
                    self.model.game_over = True
                    pygame.draw.rect(self.screen, self.light_gray, self.play_button)
                    self.screen.blit(self.buttton_object, self.button_text_rect)
                    self.reveal_word()
                    pygame.display.update()
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_button.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed()[0]:
                            # user wants to play agin
                            self.new_game()
                            print(self.model.current_word)
                            choice = True
                    clock.tick(50)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.done = True
                
                if event.type == pygame.KEYDOWN and not self.model.game_over:
                    key = pygame.key.name(event.key).upper()
                   # print(key)
                    #print(self.request_guess_count())
                    if key in self.letters and len(self.guess) < 5:
                        i = self.letters.index(key)
                        text_rect = self.text_letters[i].get_rect(center = self.grid_letter_locations[self.cur_row][self.cur_col])
                        self.screen.blit(self.text_letters[i], text_rect)
                        self.cur_col = min(4, self.cur_col + 1)
                        if len(self.guess) < 5:
                            self.guess.append(key)
                        last = "L"

                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        # Undo typing
                        #pygame.draw.rect(self.screen, self.dark_gray, [self.grid_box_locations[self.cur_row][self.cur_col][0],
                            #self.grid_box_locations[self.cur_row][self.cur_col][1], self.WIDTH, self.HEIGHT])
                        #self.cur_col =  max(0, self.cur_col - 1)

                        # Going by len of guess...
                        # This seems to be working. Fixed bug
                        pygame.draw.rect(self.screen, self.dark_gray, [self.grid_box_locations[self.cur_row][max(0, (len(self.guess) - 1))][0],
                            self.grid_box_locations[self.cur_row][self.cur_col][1], self.WIDTH, self.HEIGHT])
                        self.cur_col = max(0, (len(self.guess) - 1))
                        if self.guess:
                            self.guess.pop()
                        last = "B"

                    elif event.key == pygame.K_RETURN:
                        # send self.guess to model to check for validity
                        # do the following if valid
                        if self.validate_input_word():
                            self.display_guess(self.cur_row, "".join(self.guess))
                            self.update_keyboard()
                            if self.check_for_win():
                                #self.done = True
                                #self.new_game()
                                #continue
                                print("You Win")
                            self.cur_row = min(5, self.cur_row + 1)
                            self.cur_col = 0
                            self.guess = []
                        
            pygame.display.update()
            clock.tick(50)
        pygame.quit()

    def display_guess(self,guess_number, curr_guess):
        '''This function will take in the current_guess and
        fill in the board with that self.guess'''

        game_state = self.request_game_state()

        res = self.model.compare_single_guess(self.guess)
    
        #Y value remains constant based on current
        y = (self.MARGIN + self.HEIGHT) *guess_number + self.MARGIN
        for col in range(5): # 0 1 2 3 4

            x = 420 + (self.MARGIN + self.WIDTH) * col + self.MARGIN
            letter = self.font.render(curr_guess[col], True, self.white)
            #color = self.color_dic[game_state[curr_guess[col]]]
            color = self.color_dic[res[col]]
            t = pygame.draw.rect(self.screen, self.white, [x,y,self.WIDTH, self.HEIGHT])
            pygame.display.update()
            pygame.time.delay(200)
            r = pygame.draw.rect(self.screen, color, [x,y,self.WIDTH, self.HEIGHT])
            text_rect = letter.get_rect(center = r.center)
            self.screen.blit(letter, text_rect)
            pygame.display.update()
            
    
    def update_keyboard(self):
        '''This function will use the current self.guess to update only
            the keys that may potentially change color in the keyboard.'''
        game_state = self.request_game_state()
        guess = self.guess

        for char in guess:
            new_color = self.color_dic[game_state[char]]
            r = pygame.draw.rect(self.screen, new_color, [self.rect_dict[char][0],
             self.rect_dict[char][1], self.KEY_WIDTH, self.KEY_HEIGHT])
            letter = self.font.render(char, True, self.white)
            text_rect = letter.get_rect(center = r.center)
            self.screen.blit(letter, text_rect)
    
    def reset_keyboard(self):
        '''This method resets the keyboard'''
        color = self.light_gray
        for letter in self.letters:                 # { "Q": (x, y) }
            r = pygame.draw.rect(self.screen, color, [self.rect_dict[letter][0],
             self.rect_dict[letter][1], self.KEY_WIDTH, self.KEY_HEIGHT])
            l = self.font.render(letter, True, self.white)
            text_rect = l.get_rect(center = r.center)
            self.screen.blit(l, text_rect)
    def reset_grid(self):
        '''This method resets the word grid
            to be empty again'''
        for row in range(6):
            for col in range(5):
                x,y = self.grid_box_locations[row][col]
                pygame.draw.rect(self.screen, self.dark_gray, [x,y, self.WIDTH, self.HEIGHT])
    
    def reveal_word(self):
        word_button = pygame.Rect(130,100,150,75)
        buttton_object = self.font.render(self.model.current_word, True, self.dark_gray)
        button_text_rect = buttton_object.get_rect(center = word_button.center)

        pygame.draw.rect(self.screen, self.light_gray, word_button)
        self.screen.blit(buttton_object, button_text_rect)
    
    def hide_reveal(self):
        word_button = pygame.Rect(130,100,150,75)
        pygame.draw.rect(self.screen, self.black, word_button)

    def hide_play_button(self):
        dark_rect = self.play_button.copy()
        pygame.draw.rect(self.screen, self.black, dark_rect)


def main():
    all = ["GUESS", "HURTS", "BURNT", "MOUSE", "AISLE", "BUNTS", "KAYAK", "THINK"]
    words = ["BURNT", "GUESS", "MOUSE", "HOUSE", "TRAIN"]
    model = Wordle_Model()
    print(model.current_word)
    view = Wordle_View(model)
    view.initial_setup()
    view.run()


if __name__ == "__main__":
    main()
    


        


            