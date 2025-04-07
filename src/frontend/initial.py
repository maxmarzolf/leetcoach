import streamlit as st
from langchain.schema import HumanMessage
from react_agent.agents import ask_human
# from react_agent.graph import graph


# async def stream_graph_updates(user_input: str):
#     async for event in graph.astream({"messages": [{"role": "user", "content": user_input}]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)









async def user_input():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            await stream_graph_updates(user_input)
        except Exception as error:
            print(error)
            break



# Initialize the session state for conversation history.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("leetcoach")

# Get user input.
user_input = st.text_input("Your message:", key="input")
if st.button("Send") and user_input:
    # Process the user's input through your LangGraph application.
    bot_response = ask_human(user_input)
    
    # Append both the user input and bot response to the chat history.
    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))
    
    # Clear the text input (Streamlit reruns the script, so this helps refresh the UI).
    # st.experimental_rerun()

# Display the chat history.
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")