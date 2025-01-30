from abc import abstractmethod
import os
import time
from time import sleep

from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional
from Agents.ChatAgent import ChatAgent


class AiAgent(ChatAgent):
    def __init__(self, name: str, context: str):
        super().__init__(name)
        self.context = context
        self.setup_ai()

    @abstractmethod
    def setup_ai(self):
        """Setup the AI model and any necessary configurations"""
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response using the AI model"""
        pass

    def send_message_to_chat(self, message: str, delay: float = 0.5):
        """Send a message to Minecraft chat with support for long messages"""
        lines = message.split('\n')
        max_length = 256
        for line in lines:
            if not line.strip():
                continue
            chunks = [line[i:i + max_length] for i in range(0, len(line), max_length)]
            for chunk in chunks:
                self.post_chat(chunk.strip())
                time.sleep(delay)


class GeminiAgent(AiAgent):
    def __init__(self, name: str, context: str):
        self.model: Optional[genai.GenerativeModel] = None
        super().__init__(name, context)

    def setup_ai(self):
        """Setup Gemini AI with API key"""
        try:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                sleep(5)
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            print(f"Error setting up Gemini AI: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        """Generate response using Gemini AI"""
        try:
            full_prompt = f"{self.context}\nUser message: {prompt}"
            response = self.model.generate_content(full_prompt)
            if response and response.text:
                return response.text
            raise Exception("Empty response from Gemini")
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise

    def listen(self):
        """Override listen method from ChatMachine"""
        chat_events = self.mc.events.pollChatPosts()
        for event in chat_events:
            if event.message.startswith("@gemini"):
                self.handle_message(event.message[7:].strip())  # Remove @gemini prefix
        time.sleep(0.5)

    def handle_message(self, message: str):
        """Handle incoming messages"""
        try:
            if message:  # Only process if there's actually a message after @gemini
                response = self.generate_response(message)
                self.send_message_to_chat(response)
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            self.send_message_to_chat("Sorry, I encountered an error. Please try again.")