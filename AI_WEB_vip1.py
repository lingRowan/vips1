import streamlit as st
import openai
import random
import os
import re


openai.api_key = "sk-svcacct-8dcUrtOCCiU3jO3ysuZ29D-DeYPWd3Vk_BKZf4s5Ya-UuWekdRLkG2LzQGCKYwIT3BlbkFJ0gsmApPqJnvNjSnyvcQI7UinZ3vehK1O3RJCCCG3qAjxxlUxbFXiQTG2fZwu_AA"
model = "gpt-4o-mini"  

def generate_animal_name():
    prompt = (
        "Generate a random real life animal name and a short description of it. "
        "Do not include the name of the animal in the description. "
        "The description should focus on the animal's appearance, behavior, habitat, and diet."
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    animal_data = response['choices'][0]['message']['content'].strip().split('\n', 1)
    name = animal_data[0].strip()  
    if name.startswith("name: "):
        name = name.replace("name: ", "").strip()  

    description = animal_data[1] if len(animal_data) > 1 else "No description available."
    description = re.sub(r'[^a-zA-Z0-9 ,.!?]', '', description)  
    return name, description

def reset_session():
    st.session_state.goal, st.session_state.description = generate_animal_name()
    st.session_state.history = []
    st.session_state.guesses = 0

st.title('Welcome to our Guessing Game')
st.write("A guessing game where we provide a description, and you guess what it is.")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")

if 'goal' not in st.session_state:
    reset_session()

st.write(st.session_state.description)
#st.write(st.session_state.goal)


if 'history' not in st.session_state:
    st.session_state.history = []

for message in st.session_state.history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])



if guess := st.chat_input("Guess the object:"):
    guess = str(guess).strip().lower()  # Normalize the guess
    st.session_state.guesses += 1
    user_msg = f'Guess# {st.session_state.guesses}: {guess}'
    st.session_state.history.append({'role': 'user', 'content': user_msg})

    with st.chat_message('user'):
        st.markdown(user_msg)

    correct_answer = str(st.session_state.goal).strip().lower()
    if guess != correct_answer:
        st.error("That's not correct. Here's a hint:")
        question = f"Give me a hint about an animal that fits this description without mentioning its name: {st.session_state.description}"
        chat_completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": question}],
        )
        hint = chat_completion['choices'][0]['message']['content']
        st.write(hint)
    else:
        st.balloons()
        msg = "Congratulations! Your guess is correct! 🎉"
        st.success(msg)
        st.session_state.history.append({'role': 'assistant', 'content': msg})
        reset_session()
    