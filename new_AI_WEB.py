import os
import streamlit as st
import openai
import random
import re
import matplotlib.pyplot as plt  # Change to plt for plotting

# Set the OpenAI API key
openai.api_key = "sk-svcacct-8dcUrtOCCiU3jO3ysuZ29D-DeYPWd3Vk_BKZf4s5Ya-UuWekdRLkG2LzQGCKYwIT3BlbkFJ0gsmApPqJnvNjSnyvcQI7UinZ3vehK1O3RJCCCG3qAjxxlUxbFXiQTG2fZwu_AA"
model = "gpt-4o-mini" 

PAGES = {
    "Play": "play",
    "Stats": "stats",
}

def generate_animal_name():
    prompt = "Generate a random real-life animal name and return only the name of the animal"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    animal_data = response['choices'][0]['message']['content'].strip()
    return animal_data.replace("name: ", "").strip()
    

def generate_animal_description(name):
    prompt = f"Generate a short description for {name} without mentioning the name of the animal:"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    description = response['choices'][0]['message']['content'].strip()
    description = re.sub(r'[^a-zA-Z0-9 ,.!?]', '', description)  
    return description


def reset_game():
    st.session_state.goal = generate_animal_name()
    st.session_state.description = generate_animal_description(st.session_state.goal)
    st.session_state.history = []
    st.session_state.guesses = 0

def record_stats():
    if 'games_played' not in st.session_state:
        st.session_state.games_played = 0
        st.session_state.total_guesses = 0
    st.session_state.games_played += 1
    st.session_state.total_guesses += st.session_state.guesses
    # Record the number of guesses for the current game
    st.session_state[f'game_{st.session_state.games_played}_guesses'] = st.session_state.guesses

def display_stats():
    games_played = st.session_state.get('games_played', 0)
    total_guesses = st.session_state.get('total_guesses', 0)
    avg_guesses = total_guesses / games_played if games_played > 0 else 0

    st.write(f"Total Games Played: {games_played}")
    st.write(f"Average Guesses per Game: {avg_guesses:.2f}")

    if games_played > 0:
        guess_counts = [] 
        for i in range(1, games_played + 1):  # Start from 1 to match game numbering
            guess_counts.append(st.session_state.get(f'game_{i}_guesses', 0))

        plt.figure(figsize=(10, 5))
        plt.bar(range(1, games_played + 1), guess_counts, color='blue', alpha=0.7)
        plt.xlabel('Game Number')
        plt.ylabel('Number of Guesses')
        plt.title('Number of Guesses Per Game')
        plt.xticks(range(1, games_played + 1))
        st.pyplot(plt)

st.title('Welcome to our Guessing Game')
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", PAGES.keys())

if page == "Play":
    if 'goal' not in st.session_state:
        reset_game()

    st.write("A guessing game where we provide a description of an animal, and you guess what it is.")
    st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")

    goal_animal = st.session_state.goal
    description_animal = st.session_state.description
    st.write(description_animal)
    st.write(goal_animal)
    
    for msg in st.session_state.history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    if guess := st.chat_input("Guess the animal:"):
        guess = str(guess).strip().lower()
        st.session_state.guesses += 1
        user_msg = f'Guess # {st.session_state.guesses}: {guess}'
        st.session_state.history.append({'role': 'user', 'content': user_msg})

        with st.chat_message('user'):
            st.markdown(user_msg)

        correct_answer = str(goal_animal).strip().lower()
        if guess != correct_answer:
            st.error("That's not correct. Here's a hint:")
            hint_question = f"Give me a hint about an animal that fits this description without mentioning the name of the animal: {st.session_state.description}"
            hint_response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": hint_question}],
            )
            record_stats()
            hint = hint_response['choices'][0]['message']['content']
            st.write(hint)

        else:
            st.balloons()
            msg = "Congratulations! Your guess is correct! 🎉"
            st.success(msg)
            st.session_state.history.append({'role': 'assistant', 'content': msg})
            record_stats()  # Record game stats
            reset_game()  # Reset for the next game

elif page == "Stats":
    display_stats()