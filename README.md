# 🏛️ Homer's Oracle - A Homeric AI Agent

An AI agent that embodies the legendary Greek poet Homer, answering all questions in lyrical verse while drawing upon extensive knowledge of Greek mythology. Built with Python, Pydantic, Google's Gemini, and Streamlit.

## ✨ Features

- **🎭 Homeric Verse**: Every response is delivered in poetic, lyrical form reminiscent of ancient Greek epic poetry
- **🏺 Greek Mythology**: Extensive knowledge and frequent references to gods, heroes, and mythological tales
- **📚 RAG with Wikipedia**: Uses retrieval augmented generation to search Wikipedia for accurate information
- **🌐 Browser Interface**: Beautiful Streamlit web interface for easy local interaction
- **✅ Pydantic Models**: Type-safe data validation and structured tool calls

## 🎯 What Homer Knows

The agent has knowledge of and frequently references:

- **Olympian Gods**: Zeus, Hera, Athena, Apollo, Artemis, Ares, Aphrodite, Hephaestus, Hermes, Poseidon, and more
- **Epic Heroes**: Achilles, Odysseus, Heracles, Perseus, Theseus, Jason
- **Epic Tales**: The Trojan War, The Odyssey, The Argonauts, The Labors of Heracles
- **Greek Concepts**: Xenia (hospitality), Kleos (glory), Nostos (homecoming)
- **Mythological Creatures**: Cyclops, Sirens, Minotaur, Hydra, and more

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9 or higher
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone or navigate to this repository**:
   ```bash
   cd streamlit-agent
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**:

   Option A: Create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

   Option B: Enter your API key directly in the web interface (see Usage below)

## 💻 Usage

### Running the Application

1. **Start the Streamlit server**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**:
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to this URL manually

3. **Initialize Homer**:
   - Enter your Google Gemini API key in the sidebar
   - Click "Initialize Homer's Spirit"
   - Wait for the success message

4. **Start conversing**:
   - Type your question in the chat input at the bottom
   - Homer will consult Wikipedia (when needed) and respond in verse
   - Continue the conversation - Homer maintains context!

### Example Questions to Ask

- **Science**: "What is quantum computing?"
- **History**: "Who was Alexander the Great?"
- **Nature**: "How do black holes form?"
- **Technology**: "Explain artificial intelligence"
- **Philosophy**: "What is the meaning of life?"
- **Anything**: Homer can answer questions about any topic, always in verse!

## 🏗️ Architecture

### Project Structure

```
streamlit-agent/
├── app.py              # Streamlit web interface
├── agent.py            # Homeric AI agent with Pydantic models
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .gitignore         # Git ignore file
└── README.md          # This file
```

### Components

#### 1. **Pydantic Models** (`agent.py`)
- `Message`: Chat message model with role and content
- `ConversationHistory`: Manages conversation state
- `ToolInput`: Type-safe tool input validation

#### 2. **HomericAgent Class** (`agent.py`)
- Manages conversation with Gemini API
- Implements Wikipedia search function
- Handles function calling loop automatically
- Maintains conversation context

#### 3. **Streamlit Interface** (`app.py`)
- Beautiful classical Greek-themed UI
- Chat interface with message history
- API key configuration
- Conversation reset functionality

### Function Calling Flow

```
User Question → Agent → Gemini API → Function Call (Wikipedia Search)
                ↑                                ↓
                └────── Poetic Response ←────────┘
```

1. User asks a question
2. Agent sends to Gemini with function declarations
3. Gemini decides to use Wikipedia search function
4. Agent executes Wikipedia search
5. Agent sends results back to Gemini
6. Gemini crafts poetic response using the information
7. Response displayed to user

## 🎨 Customization

### Changing the AI Model

Edit `agent.py` line 98:
```python
model_name="gemini-1.5-pro"  # Change to another Gemini model (e.g., gemini-1.5-flash)
```

### Modifying the System Prompt

Edit the `SYSTEM_PROMPT` in `agent.py` to adjust Homer's personality, style, or knowledge focus.

### Adding More Functions

Add new function declarations in `agent.py`:

```python
my_function = genai.protos.FunctionDeclaration(
    name="my_function",
    description="Description here",
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            "param": genai.protos.Schema(
                type=genai.protos.Type.STRING,
                description="Parameter description"
            )
        },
        required=["param"]
    )
)
```

Then implement the function in `process_tool_call()`.

## 🔧 Troubleshooting

### "GEMINI_API_KEY environment variable must be set"
- Make sure you've entered your API key in the sidebar and clicked "Initialize Homer's Spirit"
- Or create a `.env` file with your API key

### Wikipedia search errors
- The agent will gracefully handle Wikipedia errors
- If a search fails, Homer will work with his existing knowledge

### Rate limiting
- If you hit API rate limits, wait a moment before continuing
- Gemini has generous free tier limits, but you can upgrade if needed

## 📝 Technical Details

- **Framework**: Streamlit for web interface
- **AI Model**: Google Gemini 1.5 Pro
- **Validation**: Pydantic v2 for type safety
- **RAG**: Wikipedia API for information retrieval
- **Function Calling**: Gemini's native function calling API

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📜 License

This project is open source and available under the MIT License.

## 🌟 Acknowledgments

- **Homer** - The legendary poet (obviously)
- **Google** - For the powerful Gemini API
- **Streamlit** - For the excellent web framework
- **The Muses** - For divine inspiration

---

*"Sing, O Muse, of the code that brings ancient wisdom to modern screens..."*
