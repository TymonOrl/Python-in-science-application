import argparse
import random
from collections import defaultdict
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Red, Gre, Yel, Blu, Pur, Cya, Whi

'''
    To start the program, use the command line:
        python wordHistogram.py <filename> -hl <histlimit> -m <minimal> -el <excludedList>
'''


def random_color():
    """Return a random color object from ascii_graph.colors."""
    available_colors = [Red, Gre, Yel, Blu, Pur, Cya, Whi]
    return random.choice(available_colors)


# Parsing Arguments
parser = argparse.ArgumentParser(description='Program processing a file to create histogram.')
parser.add_argument('filename', help='Name of the file to process')
parser.add_argument('-hl', '--histlimit', help='How many words will be shown', type=int, default=10)
parser.add_argument('-m', '--minimal', help='Minimal length limit of processed words', type=int, default=0)
parser.add_argument('-el', '--excludedList', help='List of excluded words', nargs='*', default=['', '—', ' ', '\n'])

args = parser.parse_args()
print(f'Processing file: {args.filename}')

# Creating Directories
defDict = defaultdict(int)
with open(args.filename, 'r') as file:
    for line in file:
        words = line.split()
        for word in words:
            word = word.strip('.,!?";:()[]').lower()
            if word not in args.excludedList:
                if len(word) >= args.minimal:
                    defDict[word] += 1

sorted_by_values = dict(sorted(defDict.items(), key=lambda item: item[1], reverse=True))

# Getting list for Grapth
lst_graph = []
for i in range(0, args.histlimit):
    try:
        key = list(sorted_by_values.keys())[i]
        value = sorted_by_values[key]
        lst_graph.append((key, value, random_color()))
    except IndexError:
        break

# Creating Grapth
graph = Pyasciigraph()
for line in graph.graph(f'Top {args.histlimit} most common words in {args.filename}', lst_graph):
    print(line)
