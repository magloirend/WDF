
import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from WDF.dummy_predictor import dummy_model

app = FastAPI()

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
	df = pd.read_csv('/home/victordedalus/code/magloirend/WDF/raw_data/final_df_victor.csv')
	answer = dummy_model(df, query)
	if type(answer) == str:
		return answer
	else:
		return answer.to_dict('index')

if __name__ == '__main__':
	query = input("Que cherchez-vous ? \n")
	print(get_matching_products(query))
	print(type(get_matching_products(query)))
