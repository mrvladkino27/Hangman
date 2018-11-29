# Problem Set 2, hangman.py
# Name: Valerii Buslaiev in coordination with Vladyslav Marchenko and Maksym Kurylko
# Collaborators: Valerii Buslaiev, Vladyslav Marchenko, Maksym Kurylko
# Time spent: 4 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    word_copy=set(secret_word)
    let_copy=set(letters_guessed)
    if word_copy==let_copy:
    	return True
    else:
    	return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_list=list(secret_word)
    let_gues=list(letters_guessed)
    word=[]
    for i in word_list:
    	if i not in let_gues:
    		word.append('_ ')
    	else:
    		word.append(i)
    word=''.join(word)
    return word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    guess=set(letters_guessed)
    let=set(string.ascii_lowercase)
    dif=list(let.difference(guess))
    dif.sort()
    left=''.join(dif)
    return left
	    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses=6
    warnings=3
    letters_guessed=[]

    vow={'a', 'i', 'e', 'y', 'o', 'u'}
    print("I am thinking of a word that is", len(secret_word), "letters long")
    while not is_word_guessed(secret_word, letters_guessed) and guesses>0:
        print('You have', guesses, 'guesses left.')
        print('You have', warnings, 'warnings left.')
        print('Avaliable latters:', get_available_letters(letters_guessed))
        inp=input("Please guess a letter: ")

        if inp in letters_guessed or inp not in string.ascii_lowercase:
            if warnings>0:
                warnings-=1
                print("Oops!You've already guessed that letter. You now have", warnings, "warnings:", get_guessed_word(secret_word, letters_guessed))
            else:
                guesses-=1
                print("Oops!You've already guessed that letter. You now have", guesses, "guesses:", get_guessed_word(secret_word, letters_guessed))

        elif inp in secret_word:
            letters_guessed.append(inp)
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
      
        elif inp not in secret_word:
            if inp in vow:
                guesses-=2
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            else:
                guesses-=1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print('-----------------------------------------------------')
    
    if guesses!=0:
        score=len(set(secret_word))*guesses
        print("Congratulations, you won! Your total score for this game is:", score)
    else:
        print("Ha-ha! Loooooser!")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ","")
    set_let = set(my_word)

    if len(other_word) != len(my_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != other_word[i] and my_word[i] != "_":
            return False
        elif my_word[i] == '_' and other_word[i] != '_' and other_word[i] in set_let:
        	return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    result = "Posible words: "
    for i in wordlist:
        if match_with_gaps(my_word,i):
            result += i + " "
    if len(result) == len("Posible words: "):
        return "No matches found"
    return result


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses=6
    warnings=3
    letters_guessed=[]

    vow={'a', 'i', 'e', 'y', 'o', 'u'}
    print("I am thinking of a word that is", len(secret_word), "letters long")
    while not is_word_guessed(secret_word, letters_guessed) and guesses>0:
        print('You have', guesses, 'guesses left.')
        print('You have', warnings, 'warnings left.')
        print('Avaliable latters:', get_available_letters(letters_guessed))
        inp=input("Please guess a letter: ")

        if inp=='*':
        	print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))

        elif inp in letters_guessed or inp not in string.ascii_lowercase:
            if warnings>0:
                warnings-=1
                print("Oops!You've already guessed that letter. You now have", warnings, "warnings:", get_guessed_word(secret_word, letters_guessed))
            else:
                guesses-=1
                print("Oops!You've already guessed that letter. You now have", guesses, "guesses:", get_guessed_word(secret_word, letters_guessed))

        elif inp in secret_word:
            letters_guessed.append(inp)
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
      
        elif inp not in secret_word:
            if inp in vow:
                guesses-=2
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            else:
                guesses-=1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print('-----------------------------------------------------')
    
    if guesses!=0:
        score=len(set(secret_word))*guesses
        print("Congratulations, you won! Your total score for this game is:", score)
    else:
        print("Ha-ha! Loooooser! See you later!")

# When you've completed your hangman_with_hints function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
  
    secret_word = choose_word(wordlist)
    hint = input('To run game without hints print 1. To run game with hints print 2.' )
    
    if hint=='1':
    	hangman(secret_word)

    if hint=='2':
    	hangman_with_hints(secret_word)