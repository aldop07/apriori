import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

#IRFAN NOVALDO HUANG
# Tampilan menu Market Basket Analysis
st.header('Market Basket Analysis')

# Baca data transaksi dari database
uploaded_file = st.file_uploader("Pilih file Excel yang akan diupload:")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    index_list = df.columns.tolist()
    A = st.selectbox ('Masukkan Index X / Invoice',index_list)
    B = st.selectbox ('Masukkan Index Y / Produk',index_list)
    
    # Menentukan nilai minimum support
    minimum_support = st.number_input("Nilai minimum support:",0.01)
    minimum_confidence = st.number_input("Nilai minimum confidence:",0.01)
    st.write({A})
    st.write({B})
    st.write(A)
    st.write(B)

   # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')

        #Data dibuat tabulasi
        tabular = pd.crosstab (df[A],df[B])

        # Data dibaca dengan cara encoding
        def hot_encode(x) :
            if (x<=0):
                return 0
            if (x>=1):
                return 1

        # Buat data menjadi binominal
        tabular_encode = tabular.applymap(hot_encode)
        
        # Bangun model apriori
        frq_items = apriori(tabular_encode, min_support=minimum_support, use_colnames= True)

        # Mengumpulkan aturan dalam dataframe
        rules = association_rules(frq_items, metric="confidence",min_threshold=minimum_confidence)
        rules = rules.sort_values(['confidence','lift'], ascending=[False, False])
        
        # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support","consequent support","support","confidence"]] = rules[["antecedent support","consequent support","support","confidence"]].applymap(lambda x: "{:.2f}%".format(x*100))

        # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.dataframe(rules.applymap(lambda x: ','.join(x) if type(x) == frozenset else x))
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
