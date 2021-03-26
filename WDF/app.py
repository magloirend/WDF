from dummy_predictor import dummy_model
import pandas as pd
import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


##############
## CSS #####
##############

local_css("WDF/css/style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

df = pd.read_csv("./raw_data/mag_test.csv")
st.image('WDF/css/assets/logo.svg')
search_query = st.text_input("", "un jean bleu")
df_res = dummy_model(df, str(search_query))
df_res.drop_duplicates(subset='product_id',inplace=True)
button_clicked = st.button("OK")



num =len(df_res)
if st.checkbox('Show result', False):
    for i in range(len(df_res)):
        st.image(df_res.iloc[i]['photos'],width=300,
                        caption=df_res.iloc[i]['product_name'])

##############
## dataframe user filtering #####
##############

prod_id = df_res.iloc[0]['product_id']
user_id = df_res.iloc[0]['user_id']

def filter():
    df_rec =df
    a = user_id
    df[df_rec['product_id']==prod_id]
    b =df_rec[df_rec['user_id']==a]
    if len(b)!=1:
        m = b['product_id']!= prod_id
        b.where(m).dropna(inplace =True)
        return b.where(m).dropna()[['photos','product_name']].drop_duplicates()
    else:
        return None


rec = reco = filter().head(5)

st.write(rec)
st.write('''
    ## les autres utilisateurs ont aussi commandees''')



if st.checkbox('commandees par les autres users', False):
    for i in range(len(reco)):
        st.image(reco.iloc[i]['photos'],width=300,
                        caption=reco.iloc[i]['product_name'])


# if __name__ == '__main__':
#     df = pd.read_csv("../raw_data/df_metadata_merc_24Mars.csv")
#     search_query = input('Que cherchez-vous ? (dummy model): \n')
#     print(dummy_model(df, str(search_query)))
