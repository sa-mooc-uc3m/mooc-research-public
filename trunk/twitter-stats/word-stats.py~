#!/usr/bin/python
# -*- coding: utf-8 -*-

#http://www.clips.ua.ac.be/pages/pattern-en
#http://pixelmonkey.org/pub/nlp-training/
#http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
#https://github.com/seatgeek/fuzzywuzzy
#https://gist.github.com/alexbowe/879414

__version__ = "1.0"
__authors__ = "Jose María Alvarez"
__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__contact__ = "chema.ar@gmail.com"
__date__    = "2016-02-25"

import csv
import os
import sys
import string
import re
import getopt
import collections
from sets import Set

import nltk as nltk
from nltk import cluster
from nltk.cluster import euclidean_distance
from nltk.corpus import stopwords
from numpy import array
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

lemmatizer = nltk.WordNetLemmatizer()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = self.stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word,stop_words_wn):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 < len(word) <= 40  and word.lower() not in (stop_words_wn))
    return accepted

def list_most_used_words(input_words):
	#words = flatten(map(lambda company: company.rawname.split(), companies))
	counter = collections.Counter(input_words)   #FIXME: calculate with percentiles
	return [x[0].lower() for x in filter ( lambda x: x [1] > 50,  (itertools.islice(counter.most_common(), 0, 1000)))]

def create_sentences_from_file(filename):
    raw_words = []
    for line in open(filename):
        #rawname = filter(lambda x: x in string.printable, line)
        #Be careful removing acronyms and blank spaces!
	line = line.replace("#","")
        rawname = filter(lambda x: x in string.letters or x in string.whitespace, line)
        raw_words.append(rawname) 
    return raw_words

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def create_syns_from_wn(word):
    syns = wn.synsets(word) 
    lemmas = Set()
    for syn in syns:
      lemmas = lemmas | Set([lemma.name for lemma in syn.lemmas] )
    return lemmas

def expand_list_wn(mylist):    
    source = Set(mylist)
    expanded_set = Set()
    for word in   source:
        expanded_set = expanded_set | create_syns_from_wn(word)
    return expanded_set |  source


if __name__ == "__main__":
   print "Start statistics..."
   inputfile = ''
   outputfile = ''
   args=sys.argv[1:]
   try:
      opts, args = getopt.getopt(args,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'word-stats.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'word-stats.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print "Processing: "+inputfile
   sentences = create_sentences_from_file(inputfile)
   my_stop_words= create_sentences_from_file("stop-words.txt")
   stop_words_wn = Set(stopwords.words('english'))
   stop_words_expanded = (stop_words_wn | expand_list_wn(my_stop_words))
   fd = {}
   for sentence in sentences:
	for sent in nltk.sent_tokenize(sentence):
	   for word in nltk.word_tokenize(sent):
		word = normalise(word)
		if word not in stop_words_wn:
	                try:
        	            fd[word] = fd[word]+1
        	        except KeyError:
        	            fd[word] = 1

   with open(outputfile, 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.writer(f)
    w.writerows(fd.items())

   print "End statistics..."

#sort -t, -k2 -rn output.txt | awk -F ',' '{print $1}'  > topic-frequency.txt








