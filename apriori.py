import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

#IRFAN NOVALDO HUANG
icon = 'https://th.bing.com/th/id/R.a406cbfb23b4d4937c5c3e323a7cb567?rik=4qO3lF%2ftE0LZTg&riu=http%3a%2f%2f1.bp.blogspot.com%2f-I-do3iLl5rs%2fUsuaG8IcjhI%2fAAAAAAAAAIE%2fXmXj-zTkS9U%2fs1600%2fUnsera.png&ehk=7Q%2f63voOpFTnTFwucAoLvddSl03O7NITAf9NPD3Ge7M%3d&risl=&pid=ImgRaw&r=0'
st.set_page_config(page_title="MBA", page_icon=icon)

# Tampilan menu Market Basket Analysis
st.header('Market Basket Analysis')

# Baca data transaksi dari database
xlsx = st.checkbox('xlsx')
csv = st.checkbox('csv')
uploaded_file = st.file_uploader("Pilih file Excel yang diupload:")
if uploaded_file:
    if xlsx :
        df = pd.read_excel(uploaded_file)
    else:
        pass
    if csv :
        df = pd.read_csv(uploaded_file)
    else:
        pass
    index_list = df.columns.tolist()
    A = st.selectbox ('X / Invoice',index_list)
    B = st.selectbox ('Y / Product',index_list)
    
        #all = st.checkbox('Pilih Berdasarkan Tanggal')
        #if all:
        #    C = st.selectbox('Pilih Kolom Tanggal', index_list)
        #    df[C] = pd.to_datetime(df[C])  # Mengubah kolom tanggal menjadi tipe datetime
        #    tanggal_mulai = st.date_input("Tanggal Mulai", value=pd.to_datetime(df[C]).min(), max_value=pd.to_datetime(df[C]).max())
        #    tanggal_akhir = st.date_input("Tanggal Akhir", value=pd.to_datetime(df[C]).max(), min_value=pd.to_datetime(df[C]).min())
        
        
    # Menentukan nilai minimum support
    minimum_support_percentage = st.number_input("Minimum Support: ( % )", min_value=1, max_value=100)
    minimum_support = minimum_support_percentage / 100
    minimum_confidence_percentage = st.number_input("Minimum Confidence: ( % )", min_value=1, max_value=100)
    minimum_confidence = minimum_confidence_percentage / 100

   # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')

        #if all:
        #    df = df[(df[C] >= pd.to_datetime(tanggal_mulai)) & (df[C] <= pd.to_datetime(tanggal_akhir))]
        #else:
        #    pass # jangan lakukan apapun jika tidak all dicentang
            

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
