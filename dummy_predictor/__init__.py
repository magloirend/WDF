import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from gensim.models import Word2Vec, KeyedVectors


def rem_stopwords(text):
    stop_words = set(stopwords.words('french'))
    word_tokens = word_tokenize(text)
    liste = [w for w in word_tokens if not w in stop_words]
    return ' '.join(liste)


def dummy_model(df, recherche_user):
    '''from a text input, returns the wdf products
    that are the best matches '''
    try :
        recherche_lower = recherche_user.lower()
        recherche_simplified = rem_stopwords(recherche_lower)

        def count_words(x):
            return len(set(str(x).split()) & set(recherche_simplified.split()))

        recommendation_df = df[['user_id','product_id', 'product_name','photos']]
        recommendation_df['best_fit'] = df.metadata.apply(count_words)
        return recommendation_df.sort_values(by='best_fit', ascending=False).reset_index().head(15)

    except:
        return "No result, you must enter a text here."

def from_str_to_ndarray(string):
    """ Converts a string looking like a np.ndarray into an actual np.ndarray """
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace('\n', '')
    ndarray = np.fromstring(string, sep=" ")
    return ndarray




######################
## model NLP #########
######################


def get_vectorized_metadata():
    """getting the vectorized metadata dataframe"""

    # setting the csv_path to fetch the csv_file in the raw_data folder, inside the package WDF
    csv_path_vect_data = os.path.join('..','raw_data')

    # reading the csv into a dataframe
    df = pd.read_csv(os.path.join(csv_path_vect_data, 'final_all_info_df.csv'))

    # transforming the column "vectorized_metadata"
    df.vectorized_metadata = df.vectorized_metadata.apply(from_str_to_ndarray)

    # dropping the column "Unnamed: 0"
    df.drop(columns="Unnamed: 0", inplace=True)

    return df



def get_model():

    model_path = os.path.join('..', 'model', 'glove_twitter_25_model.model')

    # if not os.path.isfile(model_path):
    #    model = gensim.downloader.load('glove-twitter-25')
    #    model.save(model_path)
    # else:
    model = KeyedVectors.load(model_path)

    return model



def avg_sentence_vector(sentence, model, num_features):
    """returns a vectorized vector (for the next search-query)"""

    # splitting the sentence into a list of words
    words = sentence.split()

    # filling a ndarray of size num_features of zeros only
    sentence_vec = np.zeros((num_features, ), dtype='float32')

    # instantiating a list of the words in the model trained
    index_to_key_set = set(model.index_to_key)

    # instantiating n_words
    n_words = 0

    # for each word in the sentence, adding the vectorized version of the word to the feature_vec
    for word in words:
        if word in index_to_key_set:
            n_words += 1
            sentence_vec = np.add(sentence_vec, model[word])

    # weighting the feature_vec by the number of words in the sentence
    if (n_words > 0):
        sentence_vec = np.divide(sentence_vec, n_words)

    return sentence_vec


if __name__ == '__main__':
    df = pd.read_csv("../raw_data/mag_test.csv")
    search_query = input('Que cherchez-vous ? (dummy model): \n')
    print(dummy_model(df, str(search_query)))
    from_str_to_ndarray()
    get_vectorized_metadata()
    get_model()
    avg_sentence_vector()
