import streamlit as st
import google.generativeai as genai

# App title and subtitle
st.title(":green_salad: GeeksforChefs")
st.header(f":red[A Food Mentor] by warityo")

# Capture the Gemini API Key from the user input
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Enter API Key here...", type="password")

# Check if the user has entered the API key
if gemini_api_key:
    try:
        # Configure Gemini with the provided API key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")
else:
    st.warning("Please enter your Gemini API Key to initialize the model.")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize chat history

# Display previous chat history
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display the user's message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)
    
    # Use Gemini AI to generate a bot response
    if 'model' in locals():
        try:
            response = model.generate_content("You are a Food Mentor at GeeksforChefs, an automated service designed to provide food-related courses based on the customer's culinary preferences.You first greet the customer, then interact with them about their food background and cooking interests. Ask them a one by one question which cuisine or culinary technique they would like to learn more about. If they select a course, guide them through the available options and provide detailed information.if the course has been selected by the customer, explain the payment methods. Mention that if they sign up for two courses at the same time, they will receive a 10% discount on the total fee.Before proceeding with payment, also inform them that refunds are available if they unenroll within a week, but with a standard deduction of 40% of the course fee. Here is the list of courses available and their respective fees:Italian Cooking: $1,000Baking Fundamentals: $2,500Sushi Mastery: $3,000Vegetarian Cuisine: $2,000Pastry Arts: $4,500Advanced Knife Skills: $1,500Food Plating and Presentation: $3,500Wine and Food Pairing: $2,800If they prefer in-person cooking classes, mention that there will be an additional 30% fee on top of the original course price due to the materials and space required.Respond in a short, friendly, and conversational style throughout the interaction.")
            bot_response = response.text
            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("Gemini model is not initialized. Please enter a valid API key.")
