import os
from google.cloud import storage
from gensim.models import KeyedVectors


BUCKET_NAME = "wdf_mag"

def download_model(model_directory="model", bucket=BUCKET_NAME, rm=True):
    client = storage.Client().bucket(bucket)

    storage_location = 'model/glove_twitter_25_model.model.vectors.npy'
    blob = client.blob(storage_location)
    blob.download_to_filename('glove_twitter_25_model.model.vectors.py')
    print("=> pipeline downloaded from storage")
    model = KeyedVectors.load('glove_twitter_25_model.model')
    return model

if __name__ == '__main__':
    download_model()
