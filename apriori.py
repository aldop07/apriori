import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Tampilan menu Apriori
st.header('Apriori')
    
# Baca data transaksi dari database
uploaded_file = st.file_uploader("Pilih file Excel yang akan diinputkan:", type=["xlsx"])
if uploaded_file is None:
    st.write("Tidak ada file yang diupload.")
    return
else:
    if uploaded_file.name.split(".")[-1] != "xlsx":
        st.error("File yang diupload harus berformat excel")
        return
try:
    df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error("Terjadi kesalahan saat membaca file, silahkan cek kembali file yang diupload")
    return

# Buat menjadi tabulasi data
A = st.text_input ('Masukan Index A')
B = st.text_input ('Masukan Index B')

try:
    if (A in df.columns) and (B in df.columns):
        tabular = pd.crosstab(df[A], df[B])
    else:
        st.error("Index tidak ditemukan")
        return
except NameError:
    st.error("Dataframe tidak ditemukan")
    return

# Menentukan nilai minimum support
minimum_support = st.number_input("Nilai minimum support:",0.01)
if minimum_support <= 0:
    st.warning("Nilai minimum support tidak boleh kosong atau nol.")
    return
    
minimum_confidence = st.number_input("Nilai minimum confidence:",0.01)
if minimum_confidence <= 0:
    st.warning("Nilai minimum confidence tidak boleh kosong atau nol.")
    return

# Bangun model apriori
frq_items = apriori(tabular_encode, min_support=minimum_support, use_colnames= True)

# Mengumpulkan aturan dalam dataframe
rules = association_rules(frq_items, metric="lift",min_threshold=minimum_confidence)
rules = rules.sort_values(['confidence','lift'], ascending=[False, False])

if st.button("PROSES"):
    st.success('HASIL PERHITUNGAN APRIORI')
        
    # Mengubah nilai support, confidence, dan lift menjadi persentase
    rules[["antecedent support","consequent support","support","confidence"]] = rules[["antecedent support","consequent support","support","confidence"]].applymap(lambda x: "{:.2f}%".format(x*100))
    
    # Menampilkan hasil algoritma apriori dalam bentuk dataframe
    st.dataframe(rules.applymap(lambda x: ','.join(x) if type(x) == frozenset else x))

