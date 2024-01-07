import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

#IRFAN NOVALDO HUANG
icon = 'https://th.bing.com/th/id/R.a406cbfb23b4d4937c5c3e323a7cb567?rik=4qO3lF%2ftE0LZTg&riu=http%3a%2f%2f1.bp.blogspot.com%2f-I-do3iLl5rs%2fUsuaG8IcjhI%2fAAAAAAAAAIE%2fXmXj-zTkS9U%2fs1600%2fUnsera.png&ehk=7Q%2f63voOpFTnTFwucAoLvddSl03O7NITAf9NPD3Ge7M%3d&risl=&pid=ImgRaw&r=0'
st.set_page_config(page_title="MBA", page_icon=icon)

# Tampilan menu Market Basket Analysis
st.header('Market Basket Analysis')

# Baca data transaksi dari database
uploaded_file = st.file_uploader("Pilih file Excel/xlsx yang diupload:")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    index_list = df.columns.tolist()
    A = st.selectbox ('X / Invoice',index_list)
    B = st.selectbox ('Y / Product',index_list)
        
    # Menentukan nilai minimum support
    minimum_support = st.number_input("Minimum Support: ( % )", max_value=100.000)
    minimum_confidence = st.number_input("Minimum Confidence: ( % )", max_value=100.000)
    
    #Data dibuat tabulasi
    tabular = pd.crosstab (df[A],df[B])

    # Fungsi untuk memberi warna kuning pada nilai > 0
    def color_positive(val):
        color = 'yellow' if val > 0 else 'white'
        return f'background-color: {color}'
    
    # Menerapkan fungsi ke seluruh DataFrame
    styled_tabular = tabular.style.applymap(color_positive)

    # Data dibaca dengan cara encoding
    def hot_encode(x) :
            if (x<=0):
                return 0
            if (x>=1):
                return 1
                
    # Buat data menjadi binominal
    tabular_encode = tabular.applymap(hot_encode)

   # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')

        # Menampilkan hasil tabulasi data dalam bentuk dataframe
        st.write('Tabulasi Data')
        st.dataframe(styled_tabular)
        st.dataframe(tabular_encode)
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
