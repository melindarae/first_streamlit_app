import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner!')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter a fruit.')
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except:
  streamlit.error('Something has gone wrong. Please try again.')

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("SELECT * FROM fruit_load_list")
  my_data_rows = my_cur.fetchall()
  return my_data_rows

if streamlit.button('Get Fruit List'):
  my_data = get_fruit_load_list()
  streamlit.dataframe(my_data)

def insert_fruit(new_fruit):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("INSERT INTO fruit_load_list values ('"+ new_fruit +"')")
  return "Thanks for adding" + new_fruit

fruit_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit'):
  row_added = insert_fruit(fruit_add)
  streamlit.write(row_added)
