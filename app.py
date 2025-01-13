import streamlit as st
import traceback
from litellm import completion
import pandas as pd
import io
import matplotlib.pyplot as plt


if "messages" not in st.session_state:
    st.session_state["messages"] = [] 

if "code_output" not in st.session_state:
    st.session_state["code_output"] = ""

if "run_code_clicked" not in st.session_state:
    st.session_state["run_code_clicked"] = False

def get_response(messages):
    
    response = completion(
        model="ollama/llama3.2:1b",
        messages=messages,
        api_base="http://localhost:11434"
    )
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

def execute_code(code):
    

    
    try:
        local_vars = {}
        exec(code, globals(), local_vars)  # Execute code
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        st.image(buffer)
        return f"Execution Successful. Output: {local_vars.get('result', 'No output variable defined')}"
    except Exception as e:
        return f"Error during execution:\n{traceback.format_exc()}"


st.title("Llama 3.2 1B Chat Demo with Code Execution")

uploaded_file  = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    dataframe  = pd.read_csv(uploaded_file)



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_input := st.chat_input("Enter your message:"):
    if  dataframe is not None:
        user_input = user_input + " " + str(dataframe)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        st.markdown("Bot")
        response_content = get_response(st.session_state.messages)
        st.markdown(response_content)

    st.session_state.messages.append({"role": "assistant", "content": response_content})

    if "```python" in response_content:
        code_block = response_content.split("```python")[1].split("```")[0].strip()
        st.session_state["current_code_block"] = code_block 
        st.markdown("### Code returned by the model:")
        st.code(code_block, language="python")

if "current_code_block" in st.session_state:
    if st.button("Run Code"):
        st.session_state.run_code_clicked = True

if st.session_state.run_code_clicked:
    code_to_run = st.session_state.get("current_code_block", "")
    st.session_state.code_output = execute_code(code_to_run)
    st.session_state.run_code_clicked = False 

if st.session_state.code_output:
    st.markdown("### Code Execution Output:")
    st.text(st.session_state.code_output)
