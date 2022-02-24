import random                                               #imports random module to randomly select a word from the word_list file
import json                                                 #imports json module to work with save data
from pathlib import Path
from termcolor import colored

wordlist = Path(__file__).with_name('word_list.txt')
savegame = Path(__file__).with_name('save_game.json')


with wordlist.open('r') as wordlist_file:
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
        self.victory = False                                    #Determines if the user has guessed the correct word
        self.exit = False                                       #Determines if the user has decided to exit or save the game
        self.word = None                                        #Initializes the word that the player has to guess
        self.letter_list = None                                 #Splits the selected word into a list which contains each letter of the word
        self.underscore_word = None                             #A List of underscores to be filled in as the player correctly guesses letters

        self.turn_count = 0                                     #Counts the amount of times the player has guessed
        self.guessed_list = []                                  #A list of all letters the player has guessed
        self.incorrect_guess_list = []                          #A list of all incorrect letters the player has guessed
        self.incorrect_guesses = 0                              #Counts the total amount of incorrect guesses
        self.incorrect_guess_limit = None                       #Sets the maximum amount of guesses the user has

        self.one = colored('[1]', 'cyan')
        self.two = colored('[2]', 'cyan')
        self.welcome()


    def welcome(self):
        print("Welcome to Hangman!")
        print("")
        print("A random word of 5-12 words will be chosen. On each turn you can guess one letter from the word. To win you must correctly guess every letter before running out of turns!")
        print("You can input \'save\' at any time to save your progress or \'exit\' to leave the game.")
        print("")
        print(self.one + " Play a new game")
        print(self.two + " Load a saved game")
        print("")

        while True:
            user_input = input()                                #Records the user's input

            if (user_input == "1"):
                self.word = self.random_word(filtered_list)     #Calls the random_word method to select a word from the filtered list
                self.letter_list = list(self.word)
                self.underscore_word = ["_"] * len(self.letter_list)
                self.incorrect_guess_limit = len(self.word)

                print("")
                print(colored(f"Your random word has been chosen, it has {len(self.word)} letters", "cyan"))
                print("")
                print("")
                self.turn()
                break                                           #Ends the loop and continues with a new game

            elif (user_input == "2"):
                self.load_progress()
                self.print_progress()
                self.turn()
                break                                           #Ends the loop and continues the game from an existing savefile

            else:
                print("Invalid input, please try again")


    def random_word(self, arg_list):
        #Generates a random integer from 0 to the length of the list given in the parameter
        word_index = random.randint(0, len(arg_list))
        return arg_list[word_index]
    

    def guess_letter(self):
        #Function to allow the user to input a letter to guess if it's within the randomly selected word
        while True:
            user_input = input()                                #Records the user's input
            user_input = user_input.lower()                     #Converts the user input to lower case to avoid case sensitivity

            #A valid input must be a single letter that has not already been guessed
            #isalpha() checks if every character is a letter from the alphabet
            if user_input.isalpha() and len(user_input)==1 and user_input not in self.guessed_list:
                self.guessed_list.append(user_input)    #Adds the inputted letter to the guessed letter list
                self.compare_letter(user_input)         #Compares the inputted letter to the randomly chosen word
                break                                   #Breaks the loop once a valid letter has been chosen and compared to the word

            elif user_input == "save":
                self.save_progress()
                self.exit = True
                break

            elif user_input == "exit":
                self.save_progress()
                self.exit = True
                break
            
            elif user_input.isalpha() and len(user_input)==1 :
                print(f"You already guessed {user_input}. Please try again.")

            else:
                print("Invalid input. Please input a single letter.")


    def compare_letter(self, letter):
        #Function that compares and checks if a letter parameter matches with any letters in the randomly selected word
        if letter in self.letter_list:
            self.replace_underscore(letter)

        else:
            self.incorrect_guess_list.append(letter)
            self.incorrect_guesses += 1
            print("")
            print(f"Incorrect guess: {letter} is not a letter in the selected word")
            self.print_progress()


    def replace_underscore(self, letter):
        #Function that replaces the blank underscores in underscore_word with letters that were correctly guessed by the user at their proper index
        index_list = [i for i, index in enumerate(self.letter_list) if index == letter]

        #Loops through the index values calculated by the enumerator and replaces the underscores at those specific indexes
        for index_value in index_list:
            self.underscore_word[index_value] = letter

        self.print_progress()


    def print_progress(self):
        #Prints the progress the user has made so far in terms of correct and incorrect guesses
        print("")
        print("")
        print("Incorrect letters gussed so far: " + colored(" ".join(self.incorrect_guess_list), "red"))
        print(colored(' '.join(self.underscore_word), 'cyan'))
        print("")

    def save_progress(self):
        #Opens the save_game.json file 
        with savegame.open("w") as savegame_file:
            #Turning all the data into a dictionary for easy json conversion
            save_data = {
                "turn": self.turn_count,
                "word": self.word,
                "word_progress": self.underscore_word,
                "guessed_letters": self.guessed_list,
                "incorrect_letters": self.incorrect_guess_list,
                "incorrect_guesses": self.incorrect_guesses
                }
            
            #Converting the dictionary to json and writing it to the save_game.json file
            savegame_file.write(json.dumps(save_data, indent=4))

    
    def load_progress(self):
        #Loads the save_game.json file
        with savegame.open("r") as savegame_file:
            save_data = json.load(savegame_file)

            self.turn_count = save_data['turn']
            self.word = save_data['word']
            self.letter_list = list(self.word)
            self.underscore_word = save_data['word_progress']
            self.guessed_list = save_data['guessed_letters']
            self.incorrect_guess_list = save_data['incorrect_letters']
            self.incorrect_guesses = save_data['incorrect_guesses']
            self.incorrect_guess_limit = len(self.word)


    def check_victory(self):
        #Compares the underscore_word list (that is having it's values be replaced by the user's correct guesses) with the original letter_list (which is the randomly selected word split into a list)
        if self.letter_list == self.underscore_word:
            self.victory = True
   

    def game_over(self):
        #Presents the user with a victory or defeat message
        if (self.victory):
            print("")
            print("Congratulations! You won!")
        else:
            print("")
            print("The word you were trying to guess was: " + self.word)
        
        self.continue_game()

    
    def continue_game(self):
        #Prompts the user if they'd like to continue playing or end the game
        print("")
        print("Would you like to play again?")
        print("")
        print(self.one + " Yes")
        print(self.two + " No")
        print("")

        #Loops continuously until the player either enters 1 or 2
        while True:
            user_input = input()                                #Records the user's input

            if (user_input == "1"):
                print("")                                       #Blank line for formatting
                Game()                                          #Launches a new game
                break                                           #Ends the loop and terminates the current game

            elif (user_input == "2"):
                break                                           #Ends the loop and terminates the current game

            else:
                print("Invalid input, please try again")


    def turn(self):
        while self.incorrect_guesses < self.incorrect_guess_limit and not self.victory and not self.exit:
            self.turn_count += 1
            self.remaining_incorrect_guesses = (self.incorrect_guess_limit - self.incorrect_guesses)

            if (self.remaining_incorrect_guesses > 3):
                print(f"You have {self.remaining_incorrect_guesses} remaining incorrect guesses.")
            else:
                print(colored(f"Think carefully! You have {self.remaining_incorrect_guesses} remaining incorrect guesses.", "red"))

            print(f"Turn {self.turn_count}: Guess one letter of the word.")
            self.guess_letter()
            self.check_victory()
        
        self.game_over()

Game()