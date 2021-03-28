import numpy as np
import pandas as pd


def from_str_to_ndarray(string):
    """ Converts a string looking like a np.ndarray into an actual np.ndarray """
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace('\n', '')
    ndarray = np.fromstring(string, sep=" ")
    return ndarray
