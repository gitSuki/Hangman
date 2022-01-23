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
        self.word = self.random_word(filtered_list)
        print(f"Your random word has been chosen, it has {len(self.word)} letters")
    
    def welcome(self):
        print("Welcome to Hangman!")
        print("")
        print("Written by gitSuki in in Python 3.8.10")
        print("")
        print("")

    def random_word(self, arg_list):
        word_index = random.randint(0, len(arg_list))
        return arg_list[word_index]

Game()