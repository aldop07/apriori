import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

#IRFAN NOVALDO
icon = 'https://th.bing.com/th/id/R.a406cbfb23b4d4937c5c3e323a7cb567?rik=4qO3lF%2ftE0LZTg&riu=http%3a%2f%2f1.bp.blogspot.com%2f-I-do3iLl5rs%2fUsuaG8IcjhI%2fAAAAAAAAAIE%2fXmXj-zTkS9U%2fs1600%2fUnsera.png&ehk=7Q%2f63voOpFTnTFwucAoLvddSl03O7NITAf9NPD3Ge7M%3d&risl=&pid=ImgRaw&r=0'
st.set_page_config(page_title="MBA", page_icon=icon)

# Tampilan menu Market Basket Analysis
st.header('Market Basket Analysis')

# Baca data transaksi dari database
uploaded_file = st.file_uploader("Pilih file Excel/xlsx yang diupload:")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Mendapatkan daftar unik dari semua kolom
    data_unik = df.stack().unique()
    item = st.multiselect('Daftar item unik yang akan di cleaning', data_unik)
    
    # Menyaring DataFrame sesuai dengan item yang dipilih
    df = df[~df.apply(lambda row: any(val in item for val in row), axis=1)]
    
    index_list = df.columns.tolist()
    A = st.selectbox('Id Transaksi', index_list)
    B = st.selectbox('Daftar Produk', index_list)
    
    # Mengambil kolom yang dipilih dari DataFrame yang sudah disaring
    produk_unik = df[B]
    
    # Mendapatkan daftar produk unik dari kolom yang dipilih
    j_produk = produk_unik.unique()
    
    # Menentukan nilai minimum support dan confidence
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

        # Transformasi DataFrame ke dalam format yang diperlukan
        transactions = df.groupby(f'{A}')[f'{B}'].apply(list).reset_index(name='Items')
        # Konversi kolom 'Items' menjadi list of lists
        dataset = transactions['Items'].tolist()

        # Gunakan mlxtend untuk mencari frequent itemsets
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df_transformed = pd.DataFrame(te_ary, columns=te.columns_)

        # Bangun model apriori
        frq_items = apriori(df_transformed, min_support=minimum_support_bagi, use_colnames=True)

        # Mengumpulkan aturan dalam dataframe
        rules = association_rules(frq_items, metric="confidence", min_threshold=minimum_confidence)

        # Hapus aturan yang memiliki kebalikan dengan confidence lebih rendah
        to_remove = set()

        for i, rule in rules.iterrows():
            antecedent = rule['antecedents']
            consequent = rule['consequents']
            reversed_rule = (consequent, antecedent, rule['confidence'], rule['support'])

            # Cek apakah aturan kebalikan sudah ada dalam set untuk dihapus
            if reversed_rule in to_remove:
                continue

            # Cek apakah aturan kebalikan sudah ada dalam DataFrame
            if any((rules['antecedents'] == set(consequent)) & (rules['consequents'] == set(antecedent))):
                # Jika aturan kebalikan sudah ada, cek confidence
                existing_indices = rules[(rules['antecedents'] == set(consequent)) & (rules['consequents'] == set(antecedent))].index
            
                # Hapus aturan yang memiliki confidence lebih rendah
                for existing_index in existing_indices:
                    if rule['confidence'] < rules.loc[existing_index, 'confidence']:
                        to_remove.add(i)
                    elif rule['confidence'] == rules.loc[existing_index, 'confidence']:
                        # Hapus aturan terakhir dengan confidence yang sama
                        if i > existing_index and i == existing_indices[-1]:
                            to_remove.add(existing_index)
            
            # Drop aturan yang memiliki kebalikan dengan confidence lebih rendah
            rules = rules.drop(to_remove)

        # Drop lift leverage dan conviction
        rules = rules.drop(['lift', 'leverage', 'conviction','zhangs_metric'], axis=1)

        # Mengubah nilai support, confidence, dan lift menjadi persentase
        rules[["antecedent support", "consequent support", "support", "confidence"]] = rules[["antecedent support", "consequent support", "support", "confidence"]].applymap(lambda x: "{:.0f}%".format(x * 100))

        # Menampilkan data nilai terbesar berada di atas
        rules = rules.sort_values(['confidence', 'support'], ascending=[False, False])

        # Menampilkan frekuensi itemset
        st.write(f'Dari total {len(j_produk)} produk yang terjual terdapat {len(frq_items)} frekuensi item pada data transaksi')
        frq_items = frq_items.sort_values(['support', ], ascending=[False])
        frq_items[["support"]] = frq_items[["support"]].applymap(lambda x: "{:.0f}%".format(x * 100))
        st.dataframe(frq_items.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))

        # Menampilkan hasil algoritma apriori dalam bentuk dataframe
        st.write(f'Ditemukan {len(rules)} Aturan Asosiasi dari total {len(dataset)} data  transaksi')
        st.table(rules.applymap(lambda x: ', '.join(x) if type(x) == frozenset else x))
        st.table(dataset)
    else:
        st.warning("Tidak ada aturan yang diproses")
else:
    st.write("Tidak ada file yang diupload.")
