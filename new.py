import time
import openai
import streamlit as st
import pandas as pd

# Initialize OpenAI API key
openai.api_key = ""

# Decorator to handle rate limit errors
def handle_rate_limit(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                # Try to call the function
                return func(*args, **kwargs)
            except openai.error.RateLimitError as e:
                # If a rate limit error occurs, wait for the specified time
                st.warning(f"Rate limit reached: {str(e)}. Waiting for 20 seconds before retrying.")
                time.sleep(20)  # Wait for 20 seconds (you can adjust the time as needed)
    return wrapper

# Function to predict gender, religion, and continent using OpenAI GPT
@handle_rate_limit
def get_gender_religion_continent(name):
    prompt = f"Given the name '{name}', predict the gender, religion, and continent of birth of the person with this name. Provide the answer in the format 'Gender: <gender>, Religion: <religion>, Continent: <continent> and continent only America,Asia,Africa,Give answer according to that continent.'"
    
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

    # User input for the CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Initialize an empty list to hold the results
        results = []
        
        # Perform predictions on each name in the CSV file
        for _, row in df.iterrows():
            name = row['name']
            gender, religion, continent = get_gender_religion_continent(name)
            results.append({'name': name, 'gender': gender, 'religion': religion, 'continent': continent})
            
        # Create a DataFrame with the results
        results_df = pd.DataFrame(results)
        
        # Display the results in a table
        st.write("Predictions:")
        st.dataframe(results_df)
        
        # Allow the user to download the results as a CSV file
        st.download_button(
            "Download results as CSV",
            results_df.to_csv(index=False).encode('utf-8'),
            file_name="results.csv",
            mime="text/csv"
        )

# Run the Streamlit app
if __name__ == "__main__":
    app()



