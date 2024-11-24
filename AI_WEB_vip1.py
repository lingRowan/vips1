import streamlit as st
from openai import OpenAI
import random

client = OpenAI(api_key="sk-svcacct-8dcUrtOCCiU3jO3ysuZ29D-DeYPWd3Vk_BKZf4s5Ya-UuWekdRLkG2LzQGCKYwIT3BlbkFJ0gsmApPqJnvNjSnyvcQI7UinZ3vehK1O3RJCCCG3qAjxxlUxbFXiQTG2fZwu_AA")
model = "gpt-4o-mini"
#question = "Do Penguins have wings?"
st.title('Welcome to our Guessing Game')
st.write("it's a simple game we will provide you with a short description of something and you have to guess what is it, if you still don't know you can always ask for more details")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")

goals_and_descriptions = {
    'dog': "I am a domesticated animal known for loyalty and companionship.",
    'cat': "I am a small domesticated feline known for hunting vermin and being independent.",
    'elephant': "I am the largest land animal with a trunk and tusks, often found in herds.",
    'penguin': "I am a flightless bird that usually lives in cold climates and waddle when I walk.",
    'giraffe': "I am known for my long neck and I eat leaves from tall trees."
}

# Initialize session state for goal and description
if 'goal' not in st.session_state:
    st.session_state.goal = random.choice(list(goals_and_descriptions.keys()))  # Randomly choose a goal from the list
    st.session_state.description = goals_and_descriptions[st.session_state.goal]  # Set description based on goal

# Streamlit app title and description
st.title('Welcome to our Guessing Game')
st.write("It's a simple game! We will provide you with a short description of something, and you have to guess what it is. If you don't know, you can always ask for more details.")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")

# Input for guessing
guess = st.text_input(label='Guess an animal')

# Handle the submission of the guess
if st.button("Submit"):
    if guess.lower() == st.session_state.goal:
        st.balloons()
        st.success("Congratulations! Your guess is correct! 🎉")
        
        # Select a new goal randomly from the keys of the dictionary and update the description
        st.session_state.goal = random.choice(list(goals_and_descriptions.keys()))
        st.session_state.description = goals_and_descriptions[st.session_state.goal]  # Set new description

        # Optionally you can display the new description to the user
        st.write("New animal description: ", st.session_state.description)

    else:
        st.error("That's not correct. Here's a hint:")
        
        # Create the question for a hint based on the current description
        question = f"Give me a hint about an animal that fits this description: {st.session_state.description}"

        # Get the hint from the OpenAI API
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question},
            ],
        )
        
        # Displaying the new hint from OpenAI
        hint = chat_completion.choices[0].message.content
        st.write(hint)