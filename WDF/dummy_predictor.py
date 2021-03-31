import numpy as np
import pandas as pd
from utils import rem_stopwords



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
