import streamlit as st
from main import initialize_agent
from langchain_community.callbacks import StreamlitCallbackHandler

st.set_page_config(
    page_title="Executive BI Agent | Monday.com", 
    page_icon="📈", 
    layout="centered"
)

with st.sidebar:
    st.header("Agent Configuration")
    st.info("""
    **Boards Connected:**
    - Deals Board (Sales Pipeline)
    - Work Order Tracker (Operations)
    
    **Engine:** Llama-3.3-70b
    **Data Source:** Live Monday.com API
    """)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

st.title("Business Intelligence Agent")
st.caption("Founder-level insights across Sales and Operations")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Enter your business query..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        
        try:
            agent_executor = initialize_agent()
            
            response = agent_executor.invoke(
                {"input": prompt, "chat_history": st.session_state.messages[:-1]},
                config={"callbacks": [st_callback]}
            )
            
            output = response["output"].replace("<br>", "\n")
            
            st.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")