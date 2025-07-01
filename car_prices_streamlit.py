import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('car_prices.csv')

# Display the original DataFrame
st.write(df)

df.shape

# Check for duplicates
st.write(f" Number of duplicate rows: {df.duplicated().sum()}")
st.write(df[df.duplicated()])
# Drop duplicates
df = df.drop_duplicates()
st.write(f"Number of duplicate rows after dropping duplicates: {df.duplicated().sum()}")

# Check and count the number of missing values (NA/null) in each column
st.write("Missing values in each column before cleaning")
st.write(df.isna().sum())

# Drop 'vin' column
df.drop(columns=['vin'], inplace=True)
st.write(f"DataFrame shape after dropping 'vin' column: {df.shape}")

# Fill missing values in 'transmission' column with the mode value
mode_value = df['transmission'].mode()[0]
df['transmission'].fillna(mode_value, inplace=True)
st.write("Missing values in each column after filling 'transmission' column")
st.write(df.isna().sum())

# Drop remaining rows with missing values
df.dropna(inplace=True)
st.write("Missing values in each column after dropping remaining rows")
st.write(df.isna().sum())

# Convert 'year' to datetime
df['year'] = pd.to_datetime(df['year'], format='%Y')

# Convert 'saledate' to datetime and keep only the date part
df['saledate'] = pd.to_datetime(df['saledate'], utc=True, format='mixed').dt.date

# Display cleaned DataFrame
st.write("### Cleaned DataFrame")
st.write(df)
df.shape


#Handling data outliers
st.write("Scatter Plot of sellingprice over year.")
st.scatter_chart(df, x="year",y="sellingprice")
st.write("Scatter Plot of condition over the year.")
st.scatter_chart(df, x="year",y="condition")


# Apply the outlier filters
df = df.loc[(df['sellingprice'] <= 175000)]
df = df.loc[(df['condition'] > 10)]

# After filtering outliers
st.write("DataFrame shape after filtering outliers:", df.shape)
st.dataframe(df)


# Function to calculate basic statistics
def calculate_statistics(data,column):
    mean = data[column].mean()
    median = data[column].median()
    std_dev = data[column].std()
    stat_column = column
    st.write(f"### Basic Statistics for {stat_column}")
    st.write(f"Mean: {mean}")
    st.write(f"Median: {median}")
    st.write(f"Standard Deviation: {std_dev}")

# Function to create a pie chart
def plot_pie_chart(data, column):
    sizes = data[column].value_counts()
    labels = sizes.index
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

#Create a function to group columns and calculate counts
def group_and_count(df, group_col, count_col):
    # Group and total quantities
    grouped_df = df.groupby(group_col)[count_col].count().reset_index()
    return grouped_df   



#A pie chart representing the car sales rate of car manufacturers in the world
st.write("### Percentage of car sales of automakers in the world")
plot_pie_chart(df, 'make')

#the best-selling car type in the Ford car brand
#Filter DataFrame by car brand 
data = df [df['make'] == 'Ford']

st.write("### The best-selling car type in the Ford car brand")
# Ratio of car models within the car brand
plot_pie_chart(data, 'model')



#The correlation between the MMR and Sellingprice
st.write("### The correlation between the MMR and Sellingprice")
st.line_chart(df, x="sellingprice", y="mmr")



#the correlation between selling price and condition
st.write("### The correlation between selling price and condition")
st.scatter_chart(df, x="condition",y="sellingprice")



#the trend in selling prices over the years
st.write("### The trend in selling prices over the years")
df_sorted =  df.sort_values(by='year', ascending=True)
st.bar_chart(df_sorted, x="year", y="sellingprice")



#The number of cars sold over the years.
salequantity = group_and_count(df, 'year', 'make')

salequantity = salequantity.rename(columns={'make': 'salequantity'})

st.write(salequantity )
st.write("### The number of cars sold over the years.")
st.bar_chart(salequantity, x="year", y="salequantity")


