import time
import pandas as pd
import streamlit as st
import openai

# Initialize OpenAI API key
openai.api_key = ""

# Function to predict gender, religion, and continent using OpenAI GPT
def get_gender_religion_continent(name):
    prompt = f"Given the name '{name}', predict the gender, religion, and continent of birth of the person with this name. Provide the answer in the format 'Gender: <gender>, Religion: <religion>, Continent: <continent>.'"
    
    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response content
    answer = response.choices[0].message.content.strip()
    
    # Initialize gender, religion, and continent as None
    gender, religion, continent = None, None, None
    
    # Parse the response
    if "Gender:" in answer and "Religion:" in answer and "Continent:" in answer:
        parts = answer.split(", ")
        gender = parts[0].split(":")[1].strip()
        religion = parts[1].split(":")[1].strip()
        continent = parts[2].split(":")[1].strip()
        
    return gender, religion, continent

# Streamlit app
def app():
    st.title("Gender, Religion, and Continent Prediction")

    # User input for the name
    name = st.text_input("Enter a name:")

    # Button to trigger the prediction
    if st.button("Predict"):
        # Perform prediction if a name is provided
        if name:
            gender, religion, continent = get_gender_religion_continent(name)
            
            # Display the results
            if gender and religion and continent:
                st.write(f"Gender: {gender}")
                st.write(f"Religion: {religion}")
                st.write(f"Continent: {continent}")
            else:
                st.write("Could not predict gender, religion, or continent. Please try again.")
        else:
            st.write("Please enter a name.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
