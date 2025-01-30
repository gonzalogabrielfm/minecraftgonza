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


class AbstractAgent(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.mc: Optional[Minecraft] = None
        self.condition: Optional[Any] = None
        self.response: Optional[Any] = None
        self.running: bool = False
        self._listener_thread: Optional[threading.Thread] = None

        try:
            self.mc = Minecraft.create()
            print(f"Agent: {self.name} connected to Minecraft server.")
        except Exception as e:
            print(f"Error connecting to Minecraft server: {e}")
            raise

    @abstractmethod
    def listen(self):
        pass

    def can_start(self) -> bool:
        return self.condition is not None and self.response is not None

    def start(self, threaded: bool = False):
        if not self.can_start():
            raise ValueError(f"Agent {self.name} is not ready to start. Set condition and response.")

        print(f"Agent: {self.name} has begun listening.")
        self.running = True

        if threaded:
            self._listener_thread = threading.Thread(target=self._run_listener)
            self._listener_thread.start()
        else:
            self._run_listener()

    def _run_listener(self):
        try:
            while self.running:
                self.listen()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(f"Agent: {self.name} interrupted.")
        except Exception as e:
            print(f"Agent {self.name} encountered an error:")
            traceback.print_exc()
        finally:
            self.running = False
            print(f"Agent: {self.name} has been shutdown.")

    def stop(self):
        """
        Modified stop method that safely handles thread shutdown
        without attempting to join from within the same thread
        """
        self.running = False  # Detiene el ciclo de escucha

        # Manejo seguro del hilo
        if self._listener_thread and threading.current_thread() is not self._listener_thread:
            self._listener_thread.join()

        # Salida del programa
        os._exit(0)  # Cierra el programa completamente
    def set_condition(self, condition: Any):
        self.condition = condition

    def set_response(self, response: Any):
        self.response = response

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def __del__(self):
        self.stop()
        if self.mc:
            self.mc.close()

