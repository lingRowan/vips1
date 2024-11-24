import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="sk-svcacct-8dcUrtOCCiU3jO3ysuZ29D-DeYPWd3Vk_BKZf4s5Ya-UuWekdRLkG2LzQGCKYwIT3BlbkFJ0gsmApPqJnvNjSnyvcQI7UinZ3vehK1O3RJCCCG3qAjxxlUxbFXiQTG2fZwu_AA")
model = "gpt-4o-mini"
#question = "Do Penguins have wings?"
st.title('Welcome to our Guessing Game')
st.write("it's a simple game we will provide you with a short description of something and you have to guess what is it, if you still don't know you can always ask for more details")
st.image("https://thumbs.dreamstime.com/z/cartoon-chat-bot-charakter-s%C3%BC%C3%9Fe-online-assistent-freundlicher-pers%C3%B6nlicher-l%C3%A4chelt-chatbot-mit-sprechblasen-l%C3%A4chelnd-sprache-241388689.jpg?ct=jpeg")
goal = 'dog'
description = "I am a domesticated animal, often known as man's best friend."
#st.write('The correct guess is: ', goal)
guess = st.text_input(label = 'Guess an thing')
if st.button("Submit"):
    if guess.lower() == goal:
        st.balloons()
        st.success("Congratulations! Your guess is correct! 🎉")
    else:
        st.error("That's not correct. Here's a hint:")
        
        # Getting an additional hint using the OpenAI model
        model = "gpt-3.5-turbo"  # Use the appropriate model you have access to
        question = f"Can you describe an animal that fits the following description: {description}?"
        
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": question},
            ],
        )
        
        # Displaying the new hint from OpenAI
        hint = chat_completion.choices[0].message.content
        st.write(hint)