import pandas as pd
import numpy as np
from scipy import spatial
from utils import *
import os
from gensim.models import KeyedVectors



def get_vectorized_metadata():
    """getting the vectorized metadata dataframe"""

    # setting the csv_path to fetch the csv_file in the raw_data folder, inside the package WDF
    csv_path_vect_data = os.path.join('raw_data')

    # reading the csv into a dataframe
    # initial df with dim 25
    #df = pd.read_csv(os.path.join(csv_path_vect_data, 'final_all_info_df.csv'))
    # df with dim 100
    df = pd.read_csv(os.path.join(csv_path_vect_data, 'final_all_info_df_100.csv'))

    # transforming the column "vectorized_metadata"
    df.metadata_100 = df.metadata_100.apply(from_str_to_ndarray)

    # dropping the column "Unnamed: 0"
    df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)

    return df



def get_model():

    # Loading the 25-dim model
    #model_path = os.path.join('model', 'glove_twitter_25_model.model')

    # Loading the 100-dim model
    model_path = os.path.join('model', 'glove_twitter_model_100.model')
    # if not os.path.isfile(model_path):
    #    model = gensim.downloader.load('glove-twitter-25')
    #    model.save(model_path)
    # else:

    model = KeyedVectors.load(model_path)

    return model



def avg_sentence_vector(sentence, model, num_features):
    """ returns a vectorized vector (for the next search-query) """

    # preprocessing of the sentence
    sentence = sentence.lower()
    sentence = removing_punctuation(sentence)
    sentence = rem_stopwords(sentence)
    sentence = lemmatizing(sentence)

    # splitting the sentence into a list of words
    words = sentence.split()

    # filling a ndarray of size num_features of zeros only
    sentence_vec = np.zeros((num_features, ), dtype='float32')

    # instantiating a list of the words in the model trained
    index_to_key_set = set(model.index_to_key)

    # instantiating a word count
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



def get_similarities_dim_25(df, search_query):
    """ returns a top-10 dataframe of the similarities between vectors in dim 25"""

    # loading the model
    model = get_model()

    # vectorizing the search query using the above function avg_sentence_vector
    search_vector = avg_sentence_vector(search_query, model, num_features=25)

    # creating a list with the similarities between the search_query vector and the vectors of the
    # products' metadata
    similarities = []
    for vector in df.vectorized_metadata:

        sim = 1 - spatial.distance.cosine(search_vector, vector)
        similarities.append(sim)

    # creating the dataframe from this list and sorting in descending order (top 10)
    similarities_df = pd.DataFrame(similarities)
    similarities_df.index = df['product_id']
    similarities_df.rename(columns={similarities_df.columns[0]: "similarities"}, inplace=True)

    similarities_df = df[['product_id', 'product_name', 'photos','price','brand_name']].merge(similarities_df, how='left', on='product_id')

    similarities_df.sort_values(by='similarities', ascending=False, inplace=True)

    return similarities_df.head(10)



def get_similarities_dim_100(df, search_query):
    """ returns a top-10 dataframe of the similarities between vectors in dim 100"""

    # loading the model
    model = get_model()

    # vectorizing the search query
    search_vector = avg_sentence_vector(search_query, model, num_features=100)


    # creating a list with the similarities between the search_query vector and the vectors of the
    # products' metadata
    similarities = []
    for vector in df.metadata_100:

        sim = 1 - spatial.distance.cosine(search_vector, vector)
        similarities.append(sim)

    # creating the dataframe from this list and sorting in descending order (top 10)
    similarities_df = pd.DataFrame(similarities)
    similarities_df.index = df['product_id']
    similarities_df.rename(columns={similarities_df.columns[0]: "similarities"}, inplace=True)

    similarities_df = df[['product_id', 'product_name', 'photos']].merge(similarities_df, how='left', on='product_id')
    similarities_df.sort_values(by='similarities', ascending=False, inplace=True)

    return similarities_df.head(10)


if __name__ == '__main__':
    df = get_vectorized_metadata()
#    print(df.head())
    search_query = input('Que cherchez-vous ? (NLP_model): \n')
#    print(get_similarities(df, search_query))
    print(get_similarities_dim_100(df, search_query))
