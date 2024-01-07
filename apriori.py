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
    df_original = pd.read_excel(uploaded_file)
    index_list = df_original.columns.tolist()
    A = st.selectbox('X / Invoice', index_list)
    B = st.selectbox('Y / Product', index_list)

    # Menentukan nilai minimum support
    minimum_support = st.number_input("Minimum Support: ( % )", 0, max_value=100)
    minimum_support = minimum_support / 100
    minimum_confidence = st.number_input("Minimum Confidence: ( % )", 0, max_value=100)
    minimum_confidence = minimum_confidence / 100
    
    # Menampilkan hasil algoritma apriori
    if st.button("PROSES"):
        st.success('HASIL PERHITUNGAN APRIORI')

        # Membersihkan nilai yang hilang
        df_original.dropna(inplace=True)

        # Membersihkan nilai yang duplikat
        df_original.drop_duplicates(inplace=True)

        if A == B or B == A:
            # Transform DataFrame to the required format
            transactions = df_original.groupby(f'{A}')[f'{B}'].apply(lambda x: ', '.join(x)).reset_index(name='Items')

            # Convert the 'Items' column to a list of lists
            dataset = transactions['Items'].apply(lambda x: [item.strip() for item in x.split(', ')]).tolist()
        else:
            # Transform DataFrame to the required format
            transactions = df_original.groupby(f'{A}')[f'{B}'].apply(list).reset_index(name='Items')

            # Convert the 'Items' column to a list of lists
            dataset = transactions['Items'].tolist()

        # Gunakan mlxtend untuk mencari frequent itemsets
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df_transformed = pd.DataFrame(te_ary, columns=te.columns_)

        # Bangun model apriori
        frq_items = apriori(df_transformed, min_support=minimum_support, use_colnames=True)

        # Mengumpulkan aturan dalam dataframe
        rules = association_rules(frq_items, metric="confidence", min_threshold=minimum_confidence)

        # Drop lift leverage dan conviction
        rules = rules.drop(['zhangs_metric', 'lift', 'leverage', 'conviction'], axis=1)

        # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support", "consequent support", "support", "confidence"]] = rules[["antecedent support", "consequent support", "support", "confidence"]].applymap(lambda x: "{:.0f}%".format(x * 100))
        
        # Menampilkan data nilai terbesar berada di atas
        rules = rules.sort_values(['confidence', 'support'], ascending=[False, False])

        # Menampilkan frekuensi itemset
        st.write('Frekuensi Item')
        frq_items = frq_items.sort_values(['support', ], ascending=[False])
        frq_items[["support"]] = frq_items[["support"]].applymap(lambda x: "{:.0f}%".format(x * 100))
        st.dataframe(frq_items.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))

        # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.write(f'Ditemukan {len(rules)} Aturan Asosiasi')
        st.dataframe(rules.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))
        st.write(f'{dataset}')
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
