from flask import Flask, render_template, request
from flask_executor import Executor
import pandas as pd
import os
import numpy as np
from scipy import spatial
import requests
from flask_json import FlaskJSON
import json
from gensim.models import Word2Vec, KeyedVectors
#from dummy_predictor import from_str_to_ndarray, get_vectorized_metadata, get_model, avg_sentence_vector
import numpy as np
from scipy import spatial
import spacy
import string
from spacy.lang.fr.stop_words import STOP_WORDS



app = Flask(__name__)
executor = Executor(app)
# json = FlaskJSON(app)

##############
## Flask #####
##############


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


def lemmatizing(text):
    """ lemmatizing a fench text """
    nlp = spacy.load('fr_core_news_md')
    doc = nlp(text)
    liste = [token.lemma_ for token in doc]
    return ' '.join(liste)


def rem_stopwords(text):
    """ Removing french stopwords from a text """
    word_split = text.split()
    stop_words = STOP_WORDS
    liste = [w for w in word_split if not w in stop_words]
    return ' '.join(liste)


def removing_punctuation(text):
    """ removing punctuation in a text """
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text




def get_vectorized_metadata():
    """getting the vectorized metadata dataframe"""

    # setting the csv_path to fetch the csv_file in the raw_data folder, inside the package WDF
    # csv_path_vect_data = os.path.join('raw_data')

    # reading the csv into a dataframe
    # initial df with dim 25
    #df = pd.read_csv(os.path.join(csv_path_vect_data, 'final_all_info_df.csv'))
    # df with dim 100
    df = pd.read_csv("WDF/data_final_all_info_df_100.csv")

    # transforming the column "vectorized_metadata"
    df.metadata_100 = df.metadata_100.apply(from_str_to_ndarray)

    # dropping the column "Unnamed: 0"
    df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)

    return df



def get_model():

    # Loading the 25-dim model
    #model_path = os.path.join('model', 'glove_twitter_25_model.model')

    # Loading the 100-dim model
    # model_path = os.path.join('model', 'glove_twitter_model_100.model')
    # if not os.path.isfile(model_path):
    #    model = gensim.downloader.load('glove-twitter-25')
    #    model.save(model_path)
    # else:

    model = KeyedVectors.load('WDF/model_glove_twitter_model_100.model')

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







@app.route('/', methods=['GET','POST'])
def my_form_post():


    df = pd.read_csv("WDF/data_final_all_info_df_100.csv")

    # transforming the column "vectorized_metadata"
    df.metadata_100 = df.metadata_100.apply(from_str_to_ndarray)

    # dropping the column "Unnamed: 0"
    df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)

    """returns a top-10 dataframe of the similarities between vectors"""
    search_query = request.args.get("text")
    sentence = str(search_query)
    model = get_model()

        # vectorizing the search query
    search_vector = avg_sentence_vector(sentence, model, num_features=100)


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

    similarities_df = df[['product_id', 'product_name', 'photos','slug','brand_name','price']].merge(similarities_df, how='left', on='product_id')
    similarities_df.sort_values(by='similarities', ascending=False, inplace=True)
    similarities_df.reset_index(inplace=True)

    query_rec = similarities_df.iloc[1]['product_name']


    search_vector_rec = avg_sentence_vector(query_rec, model, num_features=100)


        # creating a list with the similarities between the search_query vector and the vectors of the
        # products' metadata
    similarities_rec = []
    for vector in df.metadata_100:

        sim_rec = 1 - spatial.distance.cosine(search_vector_rec, vector)
        similarities_rec.append(sim_rec)

    # creating the dataframe from this list and sorting in descending order (top 10)
    similarities_df_rec = pd.DataFrame(similarities_rec)
    similarities_df_rec.index = df['product_id']
    similarities_df_rec.rename(columns={similarities_df_rec.columns[0]: "similarities"}, inplace=True)

    similarities_df_rec = df[['product_id', 'product_name', 'photos','price','brand_name','slug']].merge(similarities_df_rec, how='left', on='product_id')
    similarities_df_rec.sort_values(by='similarities', ascending=False, inplace=True)
    similarities_df_rec.reset_index(inplace=True)



    return render_template('index.html',data=similarities_df['photos'],\
        sentence=sentence,data_rec=similarities_df_rec['photos'],price=similarities_df['price'],\
        price_rec=similarities_df_rec['price'],name_rec=similarities_df_rec['product_name'],\
        slug_rec=similarities_df_rec['slug'],brand_rec=similarities_df_rec['brand_name'])

##############
## dummy model  #####
##############
request_ctx = app.test_request_context()
request_ctx.push()



if __name__ == "__main__":
    # app.run(debug=True)
     # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
