import pandas as pd
import pytest
import streamlit as st
from datetime import datetime

# Define test functions
def test_data_loading():
    df = pd.read_csv('car_prices.csv')
    assert df.shape[0] > 0, "Data loading failed"
    st.write(df)


def test_check_duplicates():
    df = pd.read_csv('car_prices.csv')
    initial_duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    final_duplicates = df.duplicated().sum()
    assert final_duplicates == 0, f"Duplicate data handling failed. Initial: {initial_duplicates}, After removal: {final_duplicates}"
    st.write(f"Initial duplicates: {initial_duplicates}, After removal: {final_duplicates}")

def test_handle_missing_values():
    df = pd.read_csv('car_prices.csv').drop(columns=['vin'])
    mode_value = df['transmission'].mode()[0]
    df['transmission'].fillna(mode_value, inplace=True)
    assert df['transmission'].isna().sum() == 0, "Missing values in 'transmission' were not filled correctly"
    st.write(df.isna().sum())

def test_drop_remaining_missing_values():
    df = pd.read_csv('car_prices.csv').drop(columns=['vin'])
    mode_value = df['transmission'].mode()[0]
    df['transmission'].fillna(mode_value, inplace=True)
    df.dropna(inplace=True)
    assert df.isna().sum().sum() == 0, "Remaining missing values were not dropped"
    st.write(df.isna().sum())

def test_convert_datetime():
    df = pd.read_csv('car_prices.csv')
    # Remove invalid year values
    current_year = datetime.now().year
    df = df[(df['year'] >= 1886) & (df['year'] <= current_year)]
    
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df['saledate'] = pd.to_datetime(df['saledate'], utc=True, errors='coerce').dt.date
    assert pd.api.types.is_datetime64_any_dtype(df['year']), "'year' was not converted to datetime"
    assert pd.api.types.is_object_dtype(df['saledate']), "'saledate' was not converted to date"
    st.write(df)

def test_filter_outliers():
    df = pd.read_csv('car_prices.csv')
    df = df.loc[(df['sellingprice'] <= 175000)]
    df = df.loc[(df['condition'] > 10)]
    assert df['sellingprice'].max() <= 175000, "Outlier values in 'sellingprice' were not filtered"
    assert df['condition'].min() > 10, "Outlier values in 'condition' were not filtered"
    st.write(df)

def test_statistical_calculations():
    df = pd.read_csv('car_prices.csv')
    mean = df['sellingprice'].mean()
    median = df['sellingprice'].median()
    std_dev = df['sellingprice'].std()
    assert mean > 0, "Mean calculation failed"
    assert median > 0, "Median calculation failed"
    assert std_dev > 0, "Standard deviation calculation failed"
    st.write(f"Mean: {mean}, Median: {median}, Standard Deviation: {std_dev}")

def test_visualizations():
    df = pd.read_csv('car_prices.csv')
    st.scatter_chart(df, x="year", y="sellingprice")
    st.write("Scatter plot created.")
    st.bar_chart(df, x="year", y="sellingprice")
    st.write("Bar chart created.")
    st.line_chart(df, x="saledate", y="sellingprice")
    st.write("Line chart created.")



# Run tests
if __name__ == "__main__":
    pytest.main()
#pytest test_car_price_analysis.py
#streamlit run test_car_price_analysis.py