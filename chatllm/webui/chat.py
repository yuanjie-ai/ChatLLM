from chatllm.llmchain.decorators import llm_stream
from meutils.pipe import *
import streamlit as st

from meutils.pipe import *
from chatllm.llmchain.llms import SparkBot

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

first_prompt = ChatPromptTemplate.from_template("{q}")

llm = SparkBot(streaming=True)
chain = LLMChain(llm=llm, prompt=first_prompt)


def on_btn_click():
    del st.session_state.messages


user_prompt = "<|User|>:{user}<eoh>\n"
robot_prompt = "<|Bot|>:{robot}<eoa>\n"
cur_query_prompt = "<|User|>:{user}<eoh>\n<|Bot|>:"


def combine_history(prompt):
    messages = st.session_state.messages
    total_prompt = ""
    for message in messages:
        cur_content = message["content"]
        if message["role"] == "user":
            cur_prompt = user_prompt.replace("{user}", cur_content)
        elif message["role"] == "robot":
            cur_prompt = robot_prompt.replace("{robot}", cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.replace("{user}", prompt)
    return total_prompt


def main():
    # torch.cuda.empty_cache()

    user_avator = "user.png"
    robot_avator = "robot.png"

    st.title("金融大模型")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user", avatar=user_avator):
            st.markdown(prompt)
        real_prompt = combine_history(prompt)
        print(f"real_prompt: {real_prompt}")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_avator})

        with st.chat_message("robot", avatar=robot_avator):
            message_placeholder = st.empty()
            cur_response = ''
            for cur_response_ in llm_stream(chain.run)(real_prompt):
                # Display robot response in chat message container
                cur_response += cur_response_
                print(cur_response)

                message_placeholder.markdown(cur_response + "▌")

            message_placeholder.markdown(cur_response)
        # Add robot response to chat history
        st.session_state.messages.append({"role": "robot", "content": cur_response, "avatar": robot_avator})


if __name__ == "__main__":
    main()
