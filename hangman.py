#imports random module to randomly select a word from the word_list file
import random

with open('word_list.txt') as wordlist_file:
    #Opens the word_list.txt file and turns each line into an entry in a list
    word_list = wordlist_file.readlines()

    #Cleans the list by stripping dead space in each entry
    cleaned_list = [word.strip() for word in word_list]

    #Creating a blank filtered list to include only words that are between 5 and 12 characters
    filtered_list = []
    for word in cleaned_list:
        if len(word) > 4 and len(word) < 13:
            filtered_list.append(word)

class Game:
    def __init__(self):
        self.welcome()
        self.turn_count = 0                                     #Turn_count counts the amount of times the player has guessed
        self.guessed_list = []                                  #A list of all the characters the played has guessed
        self.word = self.random_word(filtered_list)             #Calls the random_word method to select a word from the filtered list
        self.letter_list = list(self.word)                      #Splits the selected word into a list which contains each letter of the word
        self.guess_limit = len(self.word)                       #Sets the maximum amount of guesses the user has to correctly guess each letter
        self.underscore_word = ["_"] * len(self.letter_list)    #Creates a list of underscores to be filled in as the player correctly guesses letters

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
        #Generates a random integer from 0 to the length of the list given in the parameter
        word_index = random.randint(0, len(arg_list))
        return arg_list[word_index]
    
    def guess_letter(self):
        while True:
            user_input = input()                        #Records the user's input
            user_input = user_input.lower()             #Converts the user input to lower case to avoid case sensitivity

            #A valid input must be a single letter that has not already been guessed
            #isalpha() checks if every character is a letter from the alphabet
            if user_input.isalpha() and len(user_input)==1 and user_input not in self.guessed_list:
                self.guessed_list.append(user_input)    #Adds the inputted letter to the guessed letter list
                print(self.guessed_list)
                break

            elif user_input.isalpha() and len(user_input)==1 :
                print(f"You already guessed {user_input}. Please try again.")

            else:
                print("Invalid input. Please input a single letter.")
    
    def turn(self):
        self.turn_count += 1
        print(f"Turn {self.turn_count}: Guess one letter of the word.")
        print(f"You have {self.guess_limit} remaining incorrect guesses.")
        self.guess_letter()
        print(' '.join(self.underscore_word))

Game()