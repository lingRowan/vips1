import streamlit as st


st.title('Welcome to our Guessing Game')
st.write("it's a simple game we will provide you with a short description of an animal and you have to guess what is the animal, if you still don't know you can always ask for more details")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")
goal = 'dog'
st.write('The correct guess is: ', goal)
guess = st.text_input(label = 'Guess an animal')
if guess == goal:
    st.balloons()