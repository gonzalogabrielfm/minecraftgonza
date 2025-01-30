from abc import ABC, abstractmethod
from typing import Optional, Any
import threading
import time
import traceback
import os
import math
from typing import Tuple, Optional
from MyAdventures.mcpi.vec3 import Vec3
from MyAdventures.mcpi.minecraft import Minecraft
from Agents.AbstractAgent import AbstractAgent

class ChatAgent(AbstractAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.set_condition(self.default_con)
        self.set_response(self.default_res)

    def default_con(self, agent, event) -> bool:
        # No mockear los mensajes del propio bot para evitar loops infinitos
        return False

    def default_res(self, agent, event):
        # Obtener el mensaje original
        return 0


    def listen(self):
        chat_events = self.mc.events.pollChatPosts()
        for event in chat_events:
            if self.condition(self, event):
                if hasattr(self, 'is_silent') and self.is_silent:
                    continue  # Ignore chat events when the bot is silent
                self.response(self, event)

    def post_chat(self, message: str):
        """
        Sends a chat message to the Minecraft server with proper formatting.
        Args:
            message: The message to send
        """
        if self.mc:
            self.mc.postToChat(f"<{self.name}> {message}")
        else:
            self.log("Warning: Cannot post message - not connected to Minecraft server")

