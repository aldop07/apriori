# apriori
Apriori algorithm in python

In the above program, there are several libraries that are imported, including:

1 streamlit: A library for creating interactive web applications using Python.
2 pandas: A library for data manipulation and analysis.
3 mlxtend: A library that provides algorithms for data mining such as association rules.

Then, there are several steps that are taken in the above program, including:

1 Apriori menu display: Display the title "Apriori" on the screen.
2 Reading transaction data from an Excel file uploaded by the user.
3 Creating tabulated data using pd.crosstab() by determining the columns to be tabulated.
4 Encoding the data into binary using the hot_encode() function.
5 Determining the minimum support and minimum confidence values input by the user.
6 Building an apriori model using apriori().
7 Organizing the rules in a dataframe using association_rules().
8 Displaying the results of the apriori algorithm in a dataframe using st.dataframe().
