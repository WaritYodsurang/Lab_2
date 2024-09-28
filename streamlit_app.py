import streamlit as st
import google.generativeai as genai

# App title and subtitle
st.title("🐧 My Chatbot App")
st.subheader("Conversation")

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
            response = model.generate_content(user_input)
            bot_response = response.text
            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
    else:
        st.error("Gemini model is not initialized. Please enter a valid API key.")
