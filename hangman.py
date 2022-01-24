import random

with open('word_list.txt') as wordlist_file:
    word_list = wordlist_file.readlines()
    cleaned_list = [word.strip() for word in word_list]
    filtered_list = []
    for word in cleaned_list:
        if len(word) > 4 and len(word) < 13:
            filtered_list.append(word)


class Game:
    def __init__(self):
        self.welcome()
        self.turn_count = 0
        self.guessed_list = []
        self.word = self.random_word(filtered_list)
        self.letter_list = self.word.split()
        self.guess_limit = len(self.word)
        print(f"Your random word has been chosen, it has {len(self.word)} letters")
        print("")
        self.turn()
    
    def welcome(self):
        print("Welcome to Hangman!")
        print("")
        print("Written by gitSuki in in Python 3.8.10")
        print("")
        print("")

    def random_word(self, arg_list):
        word_index = random.randint(0, len(arg_list))
        return arg_list[word_index]
    
    def guess_letter(self):
        while True:
            user_input = input()
            user_input = user_input.lower()
            if user_input.isalpha() and user_input not in self.guessed_list:
                self.guessed_list.append(user_input)
                print(self.guessed_list)
                break
            elif user_input.isalpha():
                print(f"You already guessed {user_input}. Please try again.")
                continue
            else:
                print("Invalid input. Please input a letter.")
                continue
    
    def turn(self):
        self.turn_count += 1
        print(f"Turn {self.turn_count}: Guess one letter of the word.")
        print(f"You have {self.guess_limit} remaining incorrect guesses.")
        self.guess_letter()

Game()