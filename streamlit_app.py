# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
from requests.exceptions import JSONDecodeError

name_on_order = st.text_input("Name on Smoothie")
st.write("Your smoothie is", name_on_order)

# Write directly to the app
st.title("Customize Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want to custom your smoothie
    """)

cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
    )


if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit Order')
    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")




fruityvice_response = requests.get("http://fruitmap.org/api/trees")
st.text(fruityvice_response)

# try:
#     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#     data = fruityvice_response.json()  # This might raise JSONDecodeError
#     st.write(data)  # Display JSON data in Streamlit
#     fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=true)
# except JSONDecodeError:
#     st.error("Failed to decode JSON from the response.")
#     st.write("Response Text:", fruityvice_response.text)  # Optional: show response text for debugging
# except Exception as e:
#     st.error(f"An error occurred: {e}")
