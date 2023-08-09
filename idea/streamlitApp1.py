import streamlit as st

import streamlit as st
from story_generator import *
import time


def story_generator_interactive(prompt, history = None):
    if not history:
        history = [{"role": "system", "content": "You are a helpful ontology engineer."}]
    
    history.append({"role": "user", "content": prompt})
        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        temperature=0
    )
    response = response.choices[0].message.content

    history.append({"role": "assistant", "content": response})  # add response to conversation history
    f = open("./conversation_history.txt", "w")
    f.write(str(history))
    f.close()
    return history, response

#-----------------------------------------------------------------------------------

start_prompt = """
Context: I am a domain expert trying to create a user story to be used by ontology engineers.You are the ontology expert. 
Only ask the following question once I have responded. Ask for the specifications to generate a user story as a user of the system, which should include 
1. The Persona: What is the name of the user, what is the occupation of the user and what are their skills and interests? 
2. The Goal: What is the goal of the user?Are they facing specific issues?
3. Example Data: Do you have examples of the specific data available?
Make sure you have answers to all three questions before providing a user story.
Only ask the next question once I have responded. """

#-----------------------------------------------------------------------------------


# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful ontology engineer."}]

st.session_state.conversation_history, response1 = story_generator_interactive(start_prompt, st.session_state.conversation_history)

st.title("Interactive Story Generation Form")
st.write("""Hello! \n \
         I am your UserStoryWizard, here to help you in all the steps to create a good user story.\
         A user story contains all the requirements from the perspective of an end user of the system.
         It is a way of capturing what a user needs to achieve with a product or system, while also providing context and value.
         I am gonna guide you through each step and ask you question by question and then use your inputs to create a user story. \
         Once you are ready, start answering the following questions. \
         Once you think you provided all the information necessary, just press the\
         corresponding button below.""")

with st.chat_message("assistant"):
    st.markdown(response1)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Share your knowledge here"):
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        # with st.chat_message("assistant"):
        #     st.markdown("You just asked me this " + str(prompt))
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_history, response_new = story_generator_interactive(str(prompt), st.session_state.conversation_history)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_new)
            st.markdown("Do you have any additional information you want to provide?")
        # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_new})

print(st.session_state.conversation_history)   

if st.button('I provided all the information. Provide me the full user story.'):
    prompt = """
    Now create the full user story.The user story should be written in the following structure:

    Title: Which topics are covered by the user story?

    Persona: What is the occupation of the user and what are their goals?

    Goal:
    Keywords: provide 5-10 keywords related to the user story 
    Provide the issues a user is facing and how our application can help reach their goals.

    Scenario:
    Write out a scenario, where the user could use a structured knowledge base to help with their work.

    Example Data:

    Think of a list of requirements and provide example data for each requirement. Structure the example data by requirements
    Example data should by simple sentences.
    These are possible formats: 
    One sonata is a “Salmo alla Romana”.
    A concert played in San Pietro di Sturla for exhibition was recorded by ethnomusicologist Mauro Balma in 1994.
    The Church of San Pietro di Sturla is located in Carasco, Genova Province.
    The Sistema Ligure is described in the text “Campanari, campane e campanili di Liguria” By Mauro Balma, 1996.

    Finally, format the user story in markdown.
    """

    st.session_state.conversation_history, response_new = story_generator_interactive(str(prompt), st.session_state.conversation_history)

    st.write(response_new)
    print(response_new)
    print(st.session_state.conversation_history)
    f = open("./final_story.txt", "w")
    f.write(str(response_new))
    f.close()

