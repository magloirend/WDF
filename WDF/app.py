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


local_css("./css/style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

icon("memory")
df = pd.read_csv("../raw_data/df_metadata_merc_24Mars.csv")
search_query = st.text_input("", "un jean bleu")
df_res = dummy_model(df, str(search_query))
button_clicked = st.button("OK")
if st.checkbox('Show result', False):
    st.write(df_res)


# if __name__ == '__main__':
#     df = pd.read_csv("../raw_data/df_metadata_merc_24Mars.csv")
#     search_query = input('Que cherchez-vous ? (dummy model): \n')
#     print(dummy_model(df, str(search_query)))
