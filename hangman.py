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
        self.victory = False                                    #Determines if the user has guessed the correct word
        self.word = self.random_word(filtered_list)             #Calls the random_word method to select a word from the filtered list
        self.letter_list = list(self.word)                      #Splits the selected word into a list which contains each letter of the word
        self.underscore_word = ["_"] * len(self.letter_list)    #List of underscores to be filled in as the player correctly guesses letters

        self.turn_count = 0                                     #Counts the amount of times the player has guessed
        self.guessed_list = []                                  #A list of all letters the player has guessed
        self.incorrect_guess_list = []                          #A list of all incorrect letters the player has guessed
        self.incorrect_guesses = 0                              #Counts the total amount of incorrect guesses
        self.incorrect_guess_limit = len(self.word)             #Sets the maximum amount of guesses the user has

        print(f"Your random word has been chosen, it has {len(self.word)} letters")
        print("")
        print("")
        self.turn()


    def welcome(self):
        print("Welcome to Hangman!")
        print("")
        print("A random word of 5-12 words will be chosen. On each turn you can guess one letter from the word. To win you must correctly guess every letter before running out of turns!")
        print("")


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
        print("Incorrect letters gussed so far: " + " ".join(self.incorrect_guess_list))
        print(' '.join(self.underscore_word))
        print("")


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
            print("The word you were trying to guess was: " + self.word.under())
    
    def turn(self):
        while self.incorrect_guesses < self.incorrect_guess_limit and not self.victory:
            self.turn_count += 1
            self.remaining_incorrect_guesses = (self.incorrect_guess_limit - self.incorrect_guesses)
            print(f"Turn {self.turn_count}: Guess one letter of the word.")
            print(f"You have {self.remaining_incorrect_guesses} remaining incorrect guesses.")
            self.guess_letter()
            self.check_victory()
        
        self.game_over()

Game()