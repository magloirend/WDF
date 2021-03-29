import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


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


if __name__ == '__main__':
    df = pd.read_csv("../raw_data/mag_test.csv")
    search_query = input('Que cherchez-vous ? (dummy model): \n')
    print(dummy_model(df, str(search_query)))
