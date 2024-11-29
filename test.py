import os
import streamlit as st
import openai
import random
import re

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for security
model = "gpt-4o-mini"  

def generate_animal_name():
    prompt = "Generate a random real life animal name"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    animal_data = response['choices'][0]['message']['content'].strip().split('\n', 1)
    name = animal_data[0].replace("name: ", "").strip() 
    return name

name = generate_animal_name()

def generate_animal_name():
    prompt = "Generate a random real life animal name"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    animal_data = response['choices'][0]['message']['content'].strip()
    return animal_data.replace("name: ", "").strip()

def generate_animal_description(name):
    prompt = f"Generate a description for the animal: {name}"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    animal_data = response['choices'][0]['message']['content'].strip()
    description = re.sub(r'[^a-zA-Z0-9 ,.!?]', '', animal_data)  
    return description if description else "No description available."

def reset_session():
    st.session_state.goal = generate_animal_name()
    st.session_state.description = generate_animal_description(st.session_state.goal)
    st.session_state.history = []
    st.session_state.guesses = 0

# Initialize Streamlit app
st.title('Welcome to our Guessing Game')
st.write("A guessing game where we provide a description, and you guess what it is.")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")

if 'goal' not in st.session_state:
    reset_session()

animal_description = st.session_state.description
goal_animal = st.session_state.goal
st.write(animal_description)
st.write(goal_animal)

for message in st.session_state.history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if guess := st.chat_input("Guess the object:"):
    guess = str(guess).strip().lower()
    st.session_state.guesses += 1
    user_msg = f'Guess # {st.session_state.guesses}: {guess}'
    st.session_state.history.append({'role': 'user', 'content': user_msg})

    with st.chat_message('user'):
        st.markdown(user_msg)

    correct_answer = str(goal_animal).strip().lower()
    if guess != correct_answer:
        st.error("That's not correct. Here's a hint:")
        question = f"Give me a hint about an animal that fits this description without mentioning its name: {st.session_state.description}"
        chat_completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": question}],
            )
        hint = chat_completion['choices'][0]['message']['content']
        st.write(hint)
        st.write(goal_animal)
    else:
        st.balloons()
        msg = "Congratulations! Your guess is correct! 🎉"
        st.success(msg)
        st.session_state.history.append({'role': 'assistant', 'content': msg})
        reset_session()
