import random
from time import sleep

from Agents.ChatAgent import ChatAgent


class MinecraftChatBot:
    def __init__(self, bot_name="ChatBot"):
        """Initialize the Minecraft chatbot."""
        self.agent = ChatAgent(bot_name)

        # Set up condition to respond to specific triggers
        def chat_condition(agent, event):
            """Determine if the bot should respond to a chat message."""
            message = event.message.lower()

            if "stfu" in message:
                setattr(agent, 'is_silent', True)  # Dynamically set the agent's silent state
                print(f"Silence mode activated: {agent.is_silent}")  # Debug line
                agent.post_chat("...")  # Optional: bot says nothing or responds with a silent message
                return False  # Do not process this further
            elif "sorry" in message:
                setattr(agent, 'is_silent', False)  # Dynamically set the agent's silent state back to False
                print(f"Silence mode deactivated: {agent.is_silent}")  # Debug line
                agent.post_chat("I'm back!")
                return False  # Do not process this further

            return (
                    "@" + bot_name.lower() in message or
                    "hello" in message or
                    "bot" in message
            )

        # Set up response logic
        def chat_response(agent, event):
            """Generate a contextual response to chat messages."""
            self.agent.log("someone called me!");
            responses = [
                f"Hello!",
                f"Greetings from the Minecraft chat bot!",
                f"Did someone call me?",
                f"I'm here and ready to help!",
                f"at your service!"
            ]

            # Special command handling
            message = event.message.lower()
            if "help" in message:
                agent.post_chat(f" I can: say hello, tell a joke, or give info")
            elif "joke" in message:
                jokes = [
                    f"Why do miners make great comedians? They always dig up good material!",
                    f"What do you call a Minecraft creeper in a china shop? Explosive!",
                    f"Minecraft joke incoming: I used to be an adventurer like you..."
                ]
                agent.post_chat(random.choice(jokes))
            elif "info" in message:
                agent.post_chat(f"I'm a chat bot created to interact in Minecraft!")
            elif "kys" in message:
                agent.post_chat(f":(")
                agent.stop()

            else:
                # Random generic response
                agent.post_chat(random.choice(responses))

        # Set condition and response for the agent
        self.agent.set_condition(chat_condition)
        self.agent.set_response(chat_response)

    def start(self, threaded=True):
        """Start the chat bot agent."""
        self.agent.start(threaded)

    def stop(self):
        """Stop the chat bot agent."""
        self.agent.stop()


def main():
    """Main function to demonstrate chat bot usage."""
    global chat_bot
    try:
        # Create and start the chat bot
        chat_bot = MinecraftChatBot("Yapper")
        chat_bot.start(threaded=True)

        # Keep the main thread running
        while True:
            input("Press Enter to keep the bot running (Ctrl+C to exit)...\n")

    except KeyboardInterrupt:
        print("\nStopping Minecraft Chat Bot...")
        chat_bot.stop()


if __name__ == "__main__":
    main()