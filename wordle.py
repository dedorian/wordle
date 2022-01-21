# gonna try to make a wordle-like game

# currently just randomly writing it out, it's probably all out of whack

## libraries
import requests, random  

## global values and whatnot
word_list = []
curr_guess = ''
wordle = ' '
blank_char = ' ▀ ' 
guesses = [ [ blank_char for n in range(5) ] for _ in range(6) ]

def generate_wordle():
    ## get a list of 5-letter words
    response = requests.get('https://www.mit.edu/~ecprice/wordlist.100000')
    for word in response.content.decode('utf-8').splitlines():
        if len(word) == 5:
            word_list.append(word)

    ## return a single word from the overall list
    return random.choice(word_list)

## display gameboard in console 
def display_game(guesses): 
    print('\n'*10)
    for guess in guesses: 
        guessed_word = ''
        for char in guess:
            guessed_word += char + ' '
        print(guessed_word)  

# process inputs
def get_guess(): 
    global curr_guess 
    guess = input('Enter a 5-letter word: ')
    if guess == '': 
        print('Please enter a guess.')
        return True 
    elif guess is None: 
        print('Please enter a guess.')
        return True 
    elif len(guess) != 5:
        print('Please guess a 5-letter word.')
        return True 
    elif guess not in word_list: 
        print('Word not found in existing word list. Try again.')
        return True
    else: 
        curr_guess = guess
        return False 

def evaluate_guess(guess=curr_guess, wordle=wordle):
    global guesses
    # replaces placeholders for now, need to add upcase for right letters (or soemthing) 
    for n, guess in enumerate(guesses):
        # find the first one with a placeholder 
        if guess[0] == blank_char:
            # replace by index
            for i, char in enumerate(guess):
                # in this block, evaluate if the letter in the guess is in the wordle
                # if so, upcase in results. otherwise, downcase.
                # --
                # 'guess' is the space we're filling and enumerating over, 'curr_guess' is the current guess filling it
                # c is the character of the guess in question
                c = list(curr_guess)[i] 
                correct_letter = True if c in wordle else False 
                correct_place = True if c == list(wordle)[i] else False 

                if correct_place:
                    c = '|' + c.upper() + '|' 
                elif correct_letter: 
                    c = '|' + c.lower() + '|'
                else: 
                    c = ' ' + c.lower() + ' '

                guesses[n][i] = c
            break 

def playing():
    # an actual win
    if curr_guess == wordle:
        return False
    # oops, ran out of guesses - check everything against placeholder 
    placeholder_count = 0
    for guess in guesses: 
        if guess[0] == blank_char:
            placeholder_count += 1

    if placeholder_count > 0: 
        return True 
    else: 
        return False 

## run the game (i.e. logic loop to play)
def main(wordle = wordle):
    while playing(): 
        ## loop until an appropriate guess is made
        need_guess = True 
        while need_guess:
            display_game(guesses)
            need_guess = get_guess()
        
        evaluate_guess(curr_guess, wordle)
        ## evaluate guess. using a static variable that gets rewritten because lazy
    display_game(guesses)
    print('The winning word was ' + wordle)

## fire off main
wordle = generate_wordle()
main(wordle)
