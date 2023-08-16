import streamlit
import pandas as pd

fruits_df = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df.set_index('Fruit', inplace=True)

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
selected_fruits = streamlit.multiselect('Pick some fruits:', list(fruits_df.index), ['Avocado', 'Strawberries'])
fruits_to_show = fruits_df.loc[selected_fruits]
streamlit.dataframe(fruits_to_show)
