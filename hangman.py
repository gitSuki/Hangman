import random

with open('word_list.txt') as wordlist_file:
    word_list = wordlist_file.readlines()
    cleaned_list = [word.strip() for word in word_list]
    filtered_list = []
    for word in cleaned_list:
        if len(word) > 4 and len(word) < 13:
            filtered_list.append(word)

def random_word(arg_list):
    word_index = random.randint(0, len(arg_list))
    return arg_list[word_index]