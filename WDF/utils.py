import numpy as np
import pandas as pd
import spacy
import string
from spacy.lang.fr.stop_words import STOP_WORDS


### ### ### ### ### ### ### ### ### ###
## Processing of metadata_vectorizied #
## when reading csv                  ##
### ### ### ### ### ### ### ### ### ###

def from_str_to_ndarray(string):
    """ Converts a string looking like a np.ndarray into an actual np.ndarray """
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace('\n', '')
    ndarray = np.fromstring(string, sep=" ")
    return ndarray


### ### ### ### ### ### ### ### ### ###
## NLP words preprocessing functions ##
### ### ### ### ### ### ### ### ### ###

def removing_punctuation(text):
    """ removing punctuation in a text """
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text


def rem_stopwords(text):
    """ Removing french stopwords from a text """
    word_split = text.split()
    stop_words = STOP_WORDS
    liste = [w for w in word_split if not w in stop_words]
    return ' '.join(liste)


def lemmatizing(text):
    """ lemmatizing a fench text """
    nlp = spacy.load('fr_core_news_md')
    doc = nlp(text)
    liste = [token.lemma_ for token in doc]
    return ' '.join(liste)
