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

   # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')
        
        # Bangun model apriori
        frq_items = apriori(tabular, min_support=minimum_support, use_colnames= True)

        # Mengumpulkan aturan dalam dataframe
        rules = association_rules(frq_items, metric="confidence",min_threshold=minimum_confidence)
        rules = rules.sort_values(['confidence','lift'], ascending=[False, False])
        
        # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support","consequent support","support","confidence"]] = rules[["antecedent support","consequent support","support","confidence"]].applymap(lambda x: "{:.0f}%".format(x*100))

        # Menampilkan frekuensi itemset
        st.write('Frekuensi Item')
        frq_items[["support"]] = frq_items[["support"]].applymap(lambda x: "{:.0f}%".format(x*100))
        st.dataframe(frq_items.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))
        
        # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.write('Aturan Asosiasi')
        st.dataframe(rules.applymap(lambda x: ','.join(x) if type(x) == frozenset else x))

        # Menerapkan fungsi ke seluruh DataFrame
        styled_tabular = tabular.style.applymap(color_positive)

        # Menampilkan hasil tabulasi data dalam bentuk dataframe
        st.write('Tabulasi Data')
        st.dataframe(styled_tabular)
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
