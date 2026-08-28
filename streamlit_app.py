# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


name = st.text_input("Name on Smoothie:", "")

ingredient_list = st.multiselect("Choose up to 5 ingredients", my_dataframe, max_selections=5)



if ingredient_list:

    ingredients_string = ' '.join(ingredient_list)

    for ingredient in ingredient_list:
      st.subheader(ingredient + ' Nutrition Information')
      smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{ingredient}")  
      sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    time_to_insert = st.button("Submit Order!")
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """', '""" + name + """')"""
        #st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name}!', icon="✅")
