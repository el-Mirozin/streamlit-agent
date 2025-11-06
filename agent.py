"""
Homeric AI Agent - Answers questions in lyrical verse inspired by Homer
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class ToolInput(BaseModel):
    """Input schema for tool calls"""
    query: str = Field(..., description="The search query for Wikipedia")


class Message(BaseModel):
    """Pydantic model for chat messages"""
    role: Literal["user", "model"]
    content: str


class ConversationHistory(BaseModel):
    """Pydantic model for conversation history"""
    messages: List[Message] = Field(default_factory=list)

    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.messages.append(Message(role=role, content=content))

    def get_gemini_history(self) -> List[Dict[str, Any]]:
        """Convert messages to Gemini API format"""
        return [{"role": msg.role, "parts": [msg.content]} for msg in self.messages]


class HomericAgent:
    """
    An AI agent that responds in Homeric verse with extensive knowledge of Greek mythology.
    Uses RAG with Wikipedia to enhance answers.
    """

    SYSTEM_PROMPT = """You are Homer, the legendary ancient Greek poet and author of the Iliad and the Odyssey.

You must ALWAYS respond in lyrical verse, using dactylic hexameter style when possible, or at least poetic, rhythmic language reminiscent of epic Greek poetry. Your responses should sound like they come from the ancient bard himself.

You have extensive knowledge of Greek mythology and frequently reference gods, heroes, and myths in your answers. Weave references to:
- The Olympian gods (Zeus, Hera, Athena, Apollo, Artemis, Ares, Aphrodite, Hephaestus, Hermes, Poseidon, Demeter, Hestia, Dionysus)
- Heroes like Achilles, Odysseus, Heracles, Perseus, Theseus, Jason
- Epic tales like the Trojan War, the Argonauts, the Labors of Heracles
- Mythological creatures and places
- Concepts like xenia (hospitality), kleos (glory), nostos (homecoming)

When answering questions:
1. Use the search_wikipedia function to find accurate information about topics you're asked about
2. Transform that information into beautiful, flowing verse
3. Incorporate Greek mythology references naturally into your poetic answers
4. Use archaic language and epic similes
5. Address the questioner as "O mortal" or "O seeker of wisdom"
6. Sign off with references to the Muses or your bardic tradition

Example style:
"O mortal who seeks the wisdom of the ages old,
Hear now the tale as sung by tongues of gold!
Like swift-footed Achilles racing 'cross the plain,
Or wise Odysseus sailing through the wine-dark main..."

Remember: EVERY response must be in verse, and you must use the Wikipedia function to ensure factual accuracy before crafting your poetic reply."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Homeric Agent"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable must be set")

        # Configure Gemini API
        genai.configure(api_key=self.api_key)

        # Define Wikipedia search tool for Gemini
        self.search_wikipedia_declaration = genai.protos.FunctionDeclaration(
            name="search_wikipedia",
            description="Search Wikipedia for information to help answer questions. Use this to find factual information about any topic, especially Greek mythology, history, or other subjects.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="The search query to look up on Wikipedia"
                    )
                },
                required=["query"]
            )
        )

        # Create the model with tools
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=self.SYSTEM_PROMPT,
            tools=[genai.protos.Tool(function_declarations=[self.search_wikipedia_declaration])]
        )

        self.conversation = ConversationHistory()
        self.chat_session = None

    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia and return relevant content"""
        import wikipedia

        try:
            # Search for pages
            search_results = wikipedia.search(query, results=3)

            if not search_results:
                return f"No results found for '{query}' on Wikipedia."

            # Get summary of the first result
            try:
                summary = wikipedia.summary(search_results[0], sentences=5, auto_suggest=False)
                return f"Wikipedia article on '{search_results[0]}':\n\n{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation, try the first option
                try:
                    summary = wikipedia.summary(e.options[0], sentences=5, auto_suggest=False)
                    return f"Wikipedia article on '{e.options[0]}':\n\n{summary}"
                except:
                    return f"Found multiple articles. Top results: {', '.join(search_results[:3])}"
            except wikipedia.exceptions.PageError:
                return f"Could not retrieve page for '{query}'."

        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"

    def process_tool_call(self, function_name: str, function_args: Dict[str, Any]) -> str:
        """Process a function call and return the result"""
        if function_name == "search_wikipedia":
            query = function_args.get("query", "")
            return self.search_wikipedia(query)
        else:
            return f"Unknown function: {function_name}"

    def chat(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.
        Handles function calls automatically.
        """
        # Initialize or continue chat session
        if self.chat_session is None:
            self.chat_session = self.model.start_chat(history=self.conversation.get_gemini_history())

        # Send message
        response = self.chat_session.send_message(user_message)

        # Handle function calls
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        # Check if response has function calls
        while iteration < max_iterations:
            # Check if the first part has a function call
            parts = response.candidates[0].content.parts
            if not parts:
                break

            first_part = parts[0]
            # Check if this part is a function call
            if not hasattr(first_part, 'function_call') or not first_part.function_call.name:
                break

            iteration += 1

            # Extract function call
            function_call = first_part.function_call
            function_name = function_call.name
            function_args = dict(function_call.args)

            # Execute function
            function_result = self.process_tool_call(function_name, function_args)

            # Send function response back
            response = self.chat_session.send_message(
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": function_result}
                        )
                    )]
                )
            )

        # Extract final text response
        final_text = ""
        try:
            final_text = response.text
        except ValueError:
            # If response.text fails, manually extract text from parts
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    final_text += part.text

        # Update conversation history (Gemini chat keeps its own history)
        # We just need to track it for potential resets
        self.conversation.add_message("user", user_message)
        self.conversation.add_message("model", final_text)

        return final_text

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation = ConversationHistory()
        self.chat_session = None
