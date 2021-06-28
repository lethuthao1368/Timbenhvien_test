import streamlit as st
import pandas as pd
import numpy as np
st.title("Demo in Class")

# input
st.markdown('## Input')
is_learner = st.checkbox('Learner')
default_value_goes_here = 'Hello World'
user_input = st.text_input("Input a text", default_value_goes_here)

# output 
st.markdown('## Output')
st.write(user_input)
if is_learner:
    st.write('Hello Learner')

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])
    chart_data
"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
df

left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

start_color, end_color = st.select_slider('Select a range of color wavelength',
options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'], value=('red', 'indigo'))
st.write('You selected wavelengths between', start_color, 'and', end_color)

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider",0,1000,(100,200))
    checkbox_val = st.checkbox("Form checkbox")
# Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
st.write("Outside the form")