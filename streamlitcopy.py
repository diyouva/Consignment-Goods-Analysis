import streamlit as st
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Import custom functions from your modules
from create_index import create_index, load_data, find_similar
from hscode_similarity import get_similarity
from price_range import get_range

# Load data
df = load_data('data/cn1.csv')
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df[df['HS_CODE'].replace('', np.nan).notna()]

# def main ():
    # Title of the app
st.image(r"C:\Users\Lenovo\OneDrive\Training Data Scientist\analisis-jasa-titipan-main\analisis-jasa-titipan-main\belanja.jpg")

st.title('Consignment Note Overview')

# Replace with your Tableau embed URL
tableau_url = "https://public.tableau.com/views/BBCAudiencesTableauStyleGuide/RankTrend?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=yl"

# Embedding Tableau dashboard using iframe
st.markdown(f'<iframe src="{tableau_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)


st.sidebar.title("About")
st.sidebar.markdown("""
This app is designed to analyze and improve the Customs Declaration (CN) process 
by leveraging data analytics and machine learning models.

### Features:
- **Similar Importer Analysis:** Analyzes similarity between importers based on identification, name, and address.
- **HS Code Search:** Helps in finding HS codes based on product descriptions.
- **Price Range Prediction:** Estimates price range based on product description.

### How to Use:
1. Enter importer details and product description on the left sidebar.
2. Click on "Predict" to analyze similar importers or predict price range.
3. Use tabs to navigate between different functionalities.

For any issues or questions, please contact the app administrator.
""")

# Image to explain the goal of the app (replace with your image file path)
st.sidebar.image(r"C:\Users\Lenovo\OneDrive\Training Data Scientist\analisis-jasa-titipan-main\analisis-jasa-titipan-main\satu.jpg", caption="About the App", use_column_width=True)
st.sidebar.image(r"C:\Users\Lenovo\OneDrive\Training Data Scientist\analisis-jasa-titipan-main\analisis-jasa-titipan-main\dua.jpg", caption="About the App", use_column_width=True)

# Input from user
st.sidebar.title('Similar Importir')
no_ident = st.sidebar.text_input ('NO_IDENTITAS')
nm_penerima = st.sidebar.text_input('NAMA')
al_penerima = st.sidebar.text_input('ALAMAT PENERIMA')
uraian_barang = st.sidebar.text_input('URAIAN BARANG')

# Load data
df = load_data('./data/cn1.csv')
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df[df['HS_CODE'].replace('', np.nan).notna()]

df_hs = pd.read_csv('./data/hs_code_not_clean_id.csv', dtype=str)

# Global variables for models
model_ident = None
vectorizer_ident = None
model_name = None
vectorizer_name = None
model_address = None
vectorizer_address = None
model_uraian = None
vectorizer_uraian = None
sentence_model = None

# Function to initialize models
def initialize_models():
    global model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address, model_uraian, vectorizer_uraian, sentence_model
    model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address, model_uraian, vectorizer_uraian = create_index(df)
    sentence_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    # similar_id = find_similar(no_ident, nm_penerima, al_penerima, df, model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address)

# # Function to load HS code data and find similarity
# def load_hs_data(filepath, similar_id):
#     try:
#         df_hs = pd.read_csv(filepath, dtype=str)
#         df_hs_results = get_similarity(similar_id, sentence_model, df_hs)
#         return df_hs_results
#     except Exception as e:
#         st.error(f"Error loading HS code data: {str(e)}")
#         raise
# # Function
# ## Mencari Kemiripan Importir
# model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address, model_uraian, vectorizer_uraian = create_index(df)
# sentence_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
# similar_id = find_similar(no_ident, nm_penerima, al_penerima, df, model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address)
# similarity_penerima = similar_id[similar_id['Similarity (%)'] > 60].head(10) # get similar_id that Similarity (%) > 0.6   

# ## Mencari kesesuaian HS Code dengan Nama Produk
# df_hs = pd.read_csv('./data/hs_code_not_clean_id.csv', dtype=str)
# df_hs_results = get_similarity(similar_id, sentence_model, df_hs)

# ## Mencari range harga berdasarkan uraian produk
# range_harga = get_range(uraian_barang, df, model_uraian, vectorizer_uraian, sentence_model)
# min_harga = range_harga[0]
# max_harga = range_harga[1]

# Predict button in sidebar
if st.sidebar.button('Predict'):
    initialize_models()
    try:
        similar_id = find_similar(no_ident, nm_penerima, al_penerima, df, model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address)
        filtered_df = similar_id[similar_id['Similarity (%)'] > 60].head(10)
        st.markdown('### Filtered Similarity Results:')
        st.write(filtered_df)
    except Exception as e:
        st.markdown('### An error occurred during model prediction')
        st.write(str(e))
       
# Tabs for additional functionalities
tabs = st.sidebar.radio("Choose Prediction:", ["Price Range", "HSCode Search"])

if tabs == "Price Range":
    st.subheader("Price Range by Description")
    uraian_barang = st.text_input("Uraian Barang", key='uraian_barang_input')

    if st.button('Predict Price Range'):
        try:
            if model_uraian is None or vectorizer_uraian is None:
                initialize_models()
            range_harga = get_range(uraian_barang, df, model_uraian, vectorizer_uraian, sentence_model)
            st.write(f'Harga kisaran min: {range_harga[0]}')
            st.write(f'Harga kisaran max: {range_harga[1]}')
        except Exception as e:
            st.write(f'Error predicting price range: {str(e)}')

elif tabs == "HSCode Search":
    st.subheader("HS Code Search by Description")
    uraian_barang = st.text_input("Uraian Barang untuk HS Code")

    if st.button('Search HS Code'):
        if sentence_model is None:
            initialize_models()  # Ensure models are initialized
        try:
            similar_id = find_similar(no_ident, nm_penerima, al_penerima, df, model_ident, vectorizer_ident, model_name, vectorizer_name, model_address, vectorizer_address)
            df_hs_results = get_similarity(similar_id, sentence_model, df_hs)
            st.markdown('### HS Code Search Results:')
            st.write(df_hs_results)
        except Exception as e:
            st.error(f'Error searching for HS Code: {str(e)}')
# if __name__ == '__main__':
#     main()

