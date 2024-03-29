from dummy_predictor import dummy_model
from flask import Flask, render_template, request
from flask_executor import Executor
import pandas as pd
import os
from gensim.models import Word2Vec, KeyedVectors
from dummy_predictor import from_str_to_ndarray, get_vectorized_metadata, get_model, avg_sentence_vector
import numpy as np
from scipy import spatial

app = Flask(__name__)
executor = Executor(app)

##############
## Flask #####
##############



##############
## dummy model  #####
##############
request_ctx = app.test_request_context()
request_ctx.push()


#############
#Final model#
#############

@app.route('/', methods=['GET','POST'])
def my_form_post():

    """returns a top-10 dataframe of the similarities between vectors"""
    df = get_vectorized_metadata()
    model = get_model()
    search_query = request.args.get("text")
    sentence = str(search_query)

    # vectorizing the search query using the above function avg_sentence_vector
    search_vector = avg_sentence_vector(sentence, model, num_features=25)

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
    similarities_df.reset_index(drop=True, inplace=True)

    """reco for similar product"""


    sentence_rec = str(similarities_df.iloc[0]['product_name'])

    # vectorizing the search query using the above function avg_sentence_vector
    search_vector_rec = avg_sentence_vector(sentence_rec, model, num_features=25)

    # creating a list with the similarities between the search_query vector and the vectors of the
    # products' metadata
    similarities_rec = []
    for vector in df.vectorized_metadata:

        sim_rec = 1 - spatial.distance.cosine(search_vector_rec, vector)
        similarities_rec.append(sim_rec)

    # creating the dataframe from this list and sorting in descending order (top 10)
    similarities_df_rec = pd.DataFrame(similarities_rec)
    similarities_df_rec.index = df['product_id']
    similarities_df_rec.rename(columns={similarities_df_rec.columns[0]: "similarities"}, inplace=True)

    similarities_df_rec = df[['product_id', 'product_name', 'photos','price','brand_name','slug']].merge(similarities_df_rec, how='left', on='product_id')
    similarities_df_rec.sort_values(by='similarities', ascending=False, inplace=True)
    similarities_df_rec.reset_index(drop=True, inplace=True)

    return render_template('index.html',data=similarities_df['photos'],sentence=sentence,\
        data_rec=similarities_df_rec['photos'],price=similarities_df['price'],\
        price_rec=similarities_df_rec['price'],name_rec=similarities_df_rec['product_name'],\
        slug_rec=similarities_df_rec['slug'],brand_rec=similarities_df_rec['brand_name'])



if __name__ == "__main__":
    app.run(debug=True)
