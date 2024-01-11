import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

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
    data = st.radio("Pilih Tipe Data", ["Normalisasi","Denormalisasi"])
    A = st.selectbox('Id Transaksi', index_list)
    B = st.selectbox('Daftar Produk', index_list)
    
    # Mendapatkan daftar unik dari semua kolom
    data_unik = df.stack().unique()
    item = st.multiselect('Daftar item unik yang akan di cleaning', data_unik)
    
    # Menyaring DataFrame sesuai dengan item yang dipilih
    df = df[~df.apply(lambda row: any(val in item for val in row), axis=1)]
    
    # Menentukan nilai minimum support
    minimum_support = st.number_input("Minimum Support: ( % )", 0, max_value=100)
    minimum_support_bagi = minimum_support / 100
    minimum_confidence = st.number_input("Minimum Confidence: ( % )", 0, max_value=100)
    minimum_confidence = minimum_confidence / 100
    
    # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')

        # Membuat DataFrame baru hanya dengan kolom A dan B
        df = df[[A, B]]

        # Membersihkan nilai yang hilang
        df.dropna(inplace=True)

        # Membersihkan nilai yang duplikat
        df.drop_duplicates(inplace=True)

        if data == "Denormalisasi":
            # Konversi kolom 'Items' menjadi list of lists
            dataset = df[f'{A}'].apply(lambda x: [item.strip() for item in x.split(', ')]).tolist()
        else:
            pass
        if data == "Normalisasi":
            # Transformasi DataFrame ke dalam format yang diperlukan
            transactions = df.groupby(f'{A}')[f'{B}'].apply(list).reset_index(name='Items')
            # Konversi kolom 'Items' menjadi list of lists
            dataset = transactions['Items'].tolist()
        else:
            pass
        # Gunakan mlxtend untuk mencari frequent itemsets
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df_transformed = pd.DataFrame(te_ary, columns=te.columns_)

        # Bangun model apriori
        frq_items = apriori(df_transformed, min_support=minimum_support_bagi, use_colnames=True)

        # Mengumpulkan aturan dalam dataframe
        rules = association_rules(frq_items, metric="confidence", min_threshold=minimum_confidence)

        # Drop lift leverage dan conviction
        rules = rules.drop(['lift', 'leverage', 'conviction'], axis=1)

        # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support", "consequent support", "support", "confidence"]] = rules[["antecedent support", "consequent support", "support", "confidence"]].applymap(lambda x: "{:.0f}%".format(x * 100))
        
        # Menampilkan data nilai terbesar berada di atas
        rules = rules.sort_values(['confidence', 'support'], ascending=[False, False])

        # Menampilkan frekuensi itemset
        st.write(f'Terdapat {len(frq_items)} Frekuensi Item')
        frq_items = frq_items.sort_values(['support', ], ascending=[False])
        frq_items[["support"]] = frq_items[["support"]].applymap(lambda x: "{:.0f}%".format(x * 100))
        st.dataframe(frq_items.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))

        # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.write(f'Ditemukan {len(rules)} Aturan Asosiasi dari total {len(dataset)} data  transaksi')
        st.dataframe(rules.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
