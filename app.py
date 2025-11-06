"""
Streamlit interface for the Homeric AI Agent
"""

import streamlit as st
from agent import HomericAgent
import os

# Page configuration
st.set_page_config(
    page_title="Homer's Oracle",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more classical Greek aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #f5f5dc;
    }
    .stTextInput > div > div > input {
        background-color: #fff8dc;
        color: #2c1810;
    }
    .stChatInput > div > div > input {
        color: #2c1810;
    }
    .stButton > button {
        background-color: #8b7355;
        color: white;
        border-radius: 5px;
        border: 2px solid #8b7355;
    }
    .stButton > button:hover {
        background-color: #654321;
        border-color: #8b7355;
    }
    h1 {
        color: #8b4513;
        font-family: 'Georgia', serif;
    }
    h2, h3 {
        color: #654321;
        font-family: 'Georgia', serif;
    }
    .user-message {
        background-color: #8b7355;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #e6dcc8;
    }
    .assistant-message {
        background-color: #8b7355;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #daa520;
        font-family: 'Georgia', serif;
        font-style: italic;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False


def initialize_agent(api_key: str):
    """Initialize the Homeric agent"""
    try:
        st.session_state.agent = HomericAgent(api_key=api_key)
        st.session_state.api_key_set = True
        return True
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return False


# Header
st.title("🏛️ Homer's Oracle")
st.markdown("### *Speak with the legendary bard of ancient Greece*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚡ Divine Configuration")

    # API Key input
    st.markdown("#### Google Gemini API Key")
    api_key_input = st.text_input(
        "Enter your API key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Your Google Gemini API key is required to commune with Homer"
    )

    if st.button("Initialize Homer's Spirit"):
        if api_key_input:
            if initialize_agent(api_key_input):
                st.success("✨ Homer awakens! The muses sing!")
        else:
            st.warning("⚠️ Please provide an API key")

    st.markdown("---")

    # Reset conversation
    if st.button("🔄 Begin Anew"):
        if st.session_state.agent:
            st.session_state.agent.reset_conversation()
            st.session_state.messages = []
            st.success("The slate is cleared, like Odysseus returning home!")
        else:
            st.warning("First initialize Homer's spirit!")

    st.markdown("---")

    # Information
    st.markdown("#### 📜 About Homer's Oracle")
    st.markdown("""
    This divine agent channels the spirit of **Homer**,
    the legendary poet who sang of:

    - **The Iliad** - The wrath of Achilles and the Trojan War
    - **The Odyssey** - Odysseus's long journey home

    Homer speaks only in **lyrical verse** and draws upon
    his vast knowledge of **Greek mythology**, consulting
    the sacred scrolls of Wikipedia through divine inspiration.

    #### 🎭 Greek Mythology
    The agent knows of:
    - The Olympian gods and goddesses
    - Epic heroes and their quests
    - Mythological creatures
    - Ancient wisdom and philosophy
    """)

    st.markdown("---")
    st.markdown("#### 🌟 Example Questions")
    st.markdown("""
    - What is quantum computing?
    - Tell me about black holes
    - Who was Alexander the Great?
    - Explain photosynthesis
    - What is artificial intelligence?
    """)

# Main chat interface
if not st.session_state.api_key_set:
    st.info("👈 Please enter your Anthropic API key in the sidebar and initialize Homer's spirit to begin")
else:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">🧑 <strong>You:</strong><br>{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="assistant-message">🏛️ <strong>Homer:</strong><br>{message["content"]}</div>',
                unsafe_allow_html=True
            )

    # Chat input
    user_input = st.chat_input("Ask Homer your question, O seeker of wisdom...")

    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        st.markdown(
            f'<div class="user-message">🧑 <strong>You:</strong><br>{user_input}</div>',
            unsafe_allow_html=True
        )

        # Get response from agent
        with st.spinner("🌟 Homer consults the Muses and the sacred scrolls..."):
            try:
                response = st.session_state.agent.chat(user_input)

                # Add assistant message to chat
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Display assistant message
                st.markdown(
                    f'<div class="assistant-message">🏛️ <strong>Homer:</strong><br>{response}</div>',
                    unsafe_allow_html=True
                )

                # Force a rerun to update the chat display properly
                st.rerun()

            except Exception as e:
                st.error(f"⚠️ The gods are displeased! Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #8b7355; font-style: italic;'>
    "Sing, O Muse, of the wisdom shared by the immortal Homer..."<br>
    Built with Streamlit, Google Gemini, and the ancient art of verse
    </div>
    """,
    unsafe_allow_html=True
)
