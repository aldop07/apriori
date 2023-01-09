import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
# Tampilan menu Apriori

st.header('Apriori')
    
    # Baca data transaksi dari database MySQL
uploaded_file = st.file_uploader("Pilih file Excel yang akan diinputkan:", type=["xlsx"])
if uploaded_file is None:
    st.write("Tidak ada file yang diupload.")

df = pd.read_excel(uploaded_file, sheet_name='Sheet1')

 
    # Buat menjadi tabulasi data
A = st.text_input ('Masukan Kolom A')
B = st.text_input ('Masukan Kolom B')
tabular = pd.crosstab (df[A],df[B])

    # Data dibaca dengan cara encoding
def hot_encode(x) :
        if (x<=0):
            return 0
        if (x>=1):
            return 1

    # Buat data menjadi binominal
tabular_encode = tabular.applymap(hot_encode)

    # Menentukan nilai minimum support dan minimum confidence
minimum_support = st.number_input("Nilai minimum support:",0.0)
if minimum_support <= 0:
        st.warning("Nilai minimum support tidak boleh kosong atau nol.")

    # Bangun model apriori
frq_items = apriori(tabular_encode, min_support=minimum_support, use_colnames= True)

    # Mengumpulkan aturan dalam dataframe
rules = association_rules(frq_items, metric="lift",min_threshold=1)
rules = rules.sort_values(['confidence','lift'], ascending=[False, False])
    # Menampilkan hasil algoritma apriori
if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')
    # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support","consequent support","support","confidence"]] = rules[["antecedent support","consequent support","support","confidence"]].applymap(lambda x: "{:.2f}%".format(x*100))
    # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.dataframe(rules.applymap(lambda x: ','.join(x) if type(x) == frozenset else x))
        #st.dataframe(tabular)
