import streamlit
import pandas as pd
import requests
import snowflake.connector

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

streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about', 'Kiwi')
streamlit.write('The user entered', fruit_choice)
fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice.casefold())
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
