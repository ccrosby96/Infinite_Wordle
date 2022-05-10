import pygame
from model import Wordle_Model
from wordle_view import Wordle_View

# main entry point into Wordle Program
def main():
    model = Wordle_Model()
    view = Wordle_View(model)
    view.initial_setup()
    view.run()

if __name__ == "__main__":
    main()
    

