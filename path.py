import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initial questions
questions = [
    "Please provide your general information like name, city, state, country.",
    "Please provide your academic performance (grade, board, present percentage).",
    "What is your goal, financial position, and which places are you interested in?"
]

# Options to present after initial questions
options = [
    "Would you like a detailed roadmap to achieve your career goals considering your academics, financial status, and study locations?",
    "Do you want personalized career guidance based on your academic performance, financial status, and desired study locations?",
    "Do you need other specific guidance like scholarship opportunities, study programs, or financial planning?",
    "Other"
]

@st.cache_data
def get_ai_response(input_text, user_responses):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    # Add all user responses
    for response in user_responses:
        messages.append({"role": "user", "content": response})
    
    messages.append({"role": "user", "content": input_text})
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message['content']

def main():
    st.title("RoboTutor - Educational Chatbot")
    st.markdown("---")

    if "user_responses" not in st.session_state:
        st.session_state.user_responses = []
        st.session_state.question_index = 0

    if st.session_state.question_index < len(questions):
        user_input = st.text_input("User Input")
        if st.button("Send"):
            if user_input:
                st.session_state.user_responses.append(user_input)
                st.session_state.question_index += 1
            if st.session_state.question_index < len(questions):
                st.write(questions[st.session_state.question_index])
            else:
                st.write("Choose an option:")
                for option in options:
                    st.write(option)
    else:
        user_input = st.text_input("User Input")
        if st.button("Send"):
            if user_input:
                bot_response = get_ai_response(user_input, st.session_state.user_responses)
                st.write(bot_response)

if __name__ == "__main__":
    main()

