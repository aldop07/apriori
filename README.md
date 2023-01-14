# Apriori
Apriori algorithm in python

In the above program, there are several libraries that are imported, including:

- streamlit: A library for creating interactive web applications using Python.
- pandas: A library for data manipulation and analysis.
- mlxtend: A library that provides algorithms for data mining such as association rules.

Then, there are several steps that are taken in the above program, including:

- Apriori menu display: Display the title "Apriori" on the screen.
- Reading transaction data from an Excel file uploaded by the user.
- Creating tabulated data using pd.crosstab() by determining the columns to be tabulated.
- Encoding the data into binary using the hot_encode() function.
- Determining the minimum support and minimum confidence values input by the user.
- Building an apriori model using apriori().
- Organizing the rules in a dataframe using association_rules().
- Displaying the results of the apriori algorithm in a dataframe using st.dataframe().

ex :

https://python-mba.streamlit.app/

| Invoice | Product Name |
|---------|--------------|
| A30     | A1           |
| A30     | A3           |
| B35     | B1           |
| A02     | A1           |
| A02     | E1           |
