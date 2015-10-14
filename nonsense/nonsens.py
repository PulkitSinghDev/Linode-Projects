#!/usr/bin/env python
import random
import pickle
import cgi
import cgitb
cgitb.enable()

class Word(object):
  def __init__(self, word):
    # store the actual word
    self.word = word
    # store dict of outgoing connections (word: connection)
    self.connections = {}
    # maintain total frequency
    self.total_freq = 0

  def add_connection(self, word):
    # add a connection to the given word
    if word.word not in self.connections:
      self.connections[word.word] = Connection(word)
    else:
      self.connections[word.word].increment()
    self.total_freq += 1

  def has_next(self):
    return len(self.connections) > 0

  def select_next(self):
    # select a random successor based on frequency
    while True:
      for word in self.connections:
        if random.random() <= float(self.connections[word].count)/float(self.total_freq):
          return self.connections[word].target

class Connection(object):
  def __init__(self, target):
    # store target of connection (a Word object)
    self.target = target
    # store frequency of occurence
    self.count = 1

  def increment(self):
    # increment frequency
    self.count += 1

class Generator(object):
  def __init__(self):
    # store dict of words (word: Word)
    self.words = {}

  # process a file
  def process_file(self, file):
    f = open(file, 'r')
    for line in f:
      self.process(line)
    f.close()

  # process a text
  def process(self, txt):
    tmp = txt.split()

    for i in range(0, len(tmp)):
      # get current word
      word = tmp[i]
      # get next word
      next_word = tmp[(i+1) % len(tmp)]

      # add to generator
      self.connect_words(word, next_word)

  # add a word to the dict
  def add_word(self, word):
    if word not in self.words:
      self.words[word] = Word(word)

  # connect two words
  def connect_words(self, first, second):
    self.add_word(first)
    self.add_word(second)
    self.words[first].add_connection(self.words[second])

  # generate a sentence
  def generate(self, start, max_len):
    if start not in self.words:
	return None

    result = [start]
    current_word = self.words[start]
    while len(result) < max_len and current_word.has_next():
      current_word = current_word.select_next()
      result.append(current_word.word)

    return ' '.join(result)

# seed files
seeds = {
	'hagar': 'pg49772.txt',
	'dracula': 'pg345.txt',
	'hackers': 'hackers.txt',
	'cc': 'cc.txt',
	'mk': 'mk.txt'
}

# create generator
g = Generator()

# retrieve form data
form = cgi.FieldStorage()
start = form['start'].value
file = form['seed'].value

# check seed
if file not in seeds:
	# seed not found, set default
	file = 'hagar'

# process seed and generate
g.process_file(seeds[file])
print(g.generate(start, 256))
