from flask import Flask, render_template, request
from flask_executor import Executor
import pandas as pd
import os
import numpy as np
from scipy import spatial
import requests
from flask_json import FlaskJSON

app = Flask(__name__)
executor = Executor(app)
json = FlaskJSON(app)

##############
## Flask #####
##############

@app.route('/', methods=['GET','POST'])
def my_form_post():

    """returns a top-10 dataframe of the similarities between vectors"""
    search_query = request.args.get("text")
    sentence = str(search_query)
    url = "https://wdf100api-grg6s3f3sa-ew.a.run.app/matching_products/"
    params = {'query':f'{sentence}'}
    result = requests.get(url, params=params,timeout=None).json()
    # json_data = flask.request.json
    df_res = pd.DataFrame.from_dict(result,orient="index")

    query_rec = df_res.iloc[1]['product_name']
    params_rec = {'query':f'{query_rec}'}
    result_rec = requests.get(url, params=params_rec,timeout=None).json()
    df_res_rec = pd.DataFrame.from_dict(result_rec,orient="index")




    return render_template('index.html',data=df_res['photos'],\
        sentence=sentence,data_rec=df_res_rec['photos'],price=df_res['price'],\
        price_rec=df_res_rec['price'],name_rec=df_res_rec['product_name'],\
        slug_rec=df_res_rec['slug'],brand_rec=df_res_rec['brand_name'])

##############
## dummy model  #####
##############
request_ctx = app.test_request_context()
request_ctx.push()



if __name__ == "__main__":
    # app.run(debug=True)
     # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
