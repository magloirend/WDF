
import pandas as pd
import joblib
import sys
from os.path import join, dirname, realpath
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#parent_path = join('/home/victordedalus/code/magloirend/WDF/api', '..')  # répertoire parent du folder qu'on veut importer
#sys.path.insert(0, parent_path)

from WDF.dummy_predictor import dummy_model
from WDF.utils import from_str_to_ndarray
from WDF.NLP_model import get_similarities


app = FastAPI()
code_path = os.getenv('CODEPATH')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"ok": True}

@app.get("/matching_products/")
def get_matching_products(query):
	# loading final csv
	df = pd.read_csv(f'{code_path}/code/magloirend/WDF/raw_data/final_all_info_df.csv')
	# converting the vectorized_metadata column to the intended type
	df.vectorized_metadata = df.vectorized_metadata.apply(from_str_to_ndarray)
	answer = get_similarities(df, query)
	answer.reset_index(inplace=True)
	if type(answer) == str:
		return answer
	else:
		return answer.to_dict('index')

if __name__ == '__main__':
	query = input("Que cherchez-vous ? \n")
	print(get_matching_products(query))
	print(type(get_matching_products(query)))
