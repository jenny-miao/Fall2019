"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    possibilities = [paragraphs[i] for i in range(len(paragraphs)) if select(paragraphs[i])]

    if k >= len(possibilities):
    	return ''
    else:
    	return possibilities[k]

    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def compare(paragraph):
    	paragraph_list = paragraph.split()
    	for i in range(len(paragraph_list)):
    		paragraph_list[i] = lower(remove_punctuation(paragraph_list[i]))
    		for j in range(len(topic)):
    			if paragraph_list[i] == topic[j]:
    				return True
    	return False
    return compare

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    total = 0
    right = 0

    for i in range(min(len(typed_words), len(reference_words))):
        if typed_words[i] == reference_words[i]:
    		right += 1
    		total += 1
    	else:
    		total += 1

    if total == 0:
    	return float(0)
    return float((right / total) * 100)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    word = len(typed) / 5
    wpm = word * (60 / elapsed)
    return float(wpm)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    least = limit + 1
    least_word = user_word

    for word in valid_words:
    	difference = diff_function(user_word, word, limit)	
    	if user_word == word:
    		return user_word	
    	elif difference < least and difference <= limit:
    		least = difference
    		least_word = word

    return least_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    # assert False, 'Remove this line'
    length_diff = abs(len(goal) - len(start))
    short_len = min(len(goal), len(start))
    if limit < 0:
        return limit + 1
    elif start == goal:
        return 0
    elif len(goal) != len(start):
        return length_diff + swap_diff(start[:short_len], goal[:short_len], limit - length_diff)
    else:
        if start[-1] == goal[-1]:
            return swap_diff(start[:-1], goal[:-1], limit)
        else:
            return 1 + swap_diff(start[:-1], goal[:-1], limit - 1)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    # assert False, 'Remove this line'

    if start == goal:
        return 0
    if limit < 0:
        return 1
    elif start == "":
        return len(goal)
    elif goal == "":
        return len(start)

    add_diff = lambda start, goal, limit: 1 + edit_diff(start, goal[1:], limit - 1) 
    remove_diff = lambda start, goal, limit: 1 + edit_diff(start[1:], goal, limit - 1) 
    substitute_diff = lambda start, goal, limit: 1 + edit_diff(start[1:], goal[1:], limit - 1) if start[0] != goal[0] else edit_diff(start[1:], goal[1:], limit)


    return min(add_diff(start, goal, limit), remove_diff(start, goal, limit), substitute_diff(start, goal, limit))
       


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    correct = 0
    match = True
    for i in range(len(typed)):
        if match:           
            if typed[i] == prompt[i]:
                correct += 1
            else:
                match = False

    progress = correct / len(prompt)
    send({'id': id, 'progress': progress})
    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    def typing_time(play_num, i): # i = indice of word
        if i == 0:
            return elapsed_time(word_times[play_num][i])
        return elapsed_time(word_times[play_num][i]) - elapsed_time(word_times[play_num][i - 1])

    def compare(play_num):
        lst = []
        for i in range(n_words):
            smallest = True
            for j in range(n_players):
                if typing_time(play_num, i + 1) > (typing_time(j, i + 1) + margin):
                    smallest = False
            if smallest == True:
                lst += [word(word_times[play_num][i + 1])]
        return lst

    total_lst = []
    for player in range(n_players):
        total_lst += [compare(player)]
    return total_lst

def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)