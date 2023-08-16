import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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


def get_fruity_vice_data(fruit_choice):
  fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice.casefold())
  return pd.json_normalize(fruityvice_response.json())


streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fruityvice_normalized = get_fruity_vice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()


streamlit.header("The fruit data load contains:")


def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values (%s)", (new_fruit,))
    return "Thanks for adding " + new_fruit
    

fruit_to_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add Fruit to the List):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  text_after_add = insert_row_snowflake(fruit_to_add)
  streamlit.text(text_after_add)
