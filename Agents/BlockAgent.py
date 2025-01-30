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


class BlockAgent(AbstractAgent):
    def __init__(self, name: str, block_id: int, block_data: int = 0):
        super().__init__(name)
        self.block_id = block_id
        self.block_data = block_data
        self.current_pos: Optional[Vec3] = None
        self.target_player_id = None
        self.follow_distance = 3  # Distancia ideal para seguir al jugador
        self.max_distance = 5  # Distancia máxima antes de teletransportarse
        self.min_distance = 2  # Distancia mínima para mantener
        self.set_condition(self.default_con)
        self.set_response(self.default_res)

    def default_con(self, agent, event) -> bool:
        # No mockear los mensajes del propio bot para evitar loops infinitos
        return False

    def default_res(self, agent, event):
        # Obtener el mensaje original
        return 0

    def listen(self):
        """Monitorea la posición del jugador y actualiza la posición del bloque."""
        if self.target_player_id is None:
            # Si no hay jugador objetivo, obtiene el primer jugador que encuentra
            players = self.mc.getPlayerEntityIds()
            if players:
                self.target_player_id = players[0]
                self.log(f"Siguiendo al jugador ID: {self.target_player_id}")
            return

        try:
            player_pos = Vec3(*self.mc.entity.getPos(self.target_player_id))

            if self.current_pos is None:
                # Primera colocación del bloque
                self.place_initial_block(player_pos)
            else:
                # Actualiza la posición si es necesario
                self.update_block_position(player_pos)

        except Exception as e:
            self.log(f"Error al seguir al jugador: {e}")

    def place_initial_block(self, player_pos: Vec3):
        """Coloca el bloque por primera vez cerca del jugador."""
        # Coloca el bloque a la distancia ideal detrás del jugador
        pos = self.calculate_position(player_pos)
        self.place_block(pos)
        self.current_pos = pos

    def calculate_position(self, player_pos: Vec3) -> Vec3:
        """Calcula la mejor posición para el bloque relativa al jugador."""
        # Obtiene la dirección en la que mira el jugador
        player_rotation = self.mc.entity.getRotation(self.target_player_id)

        # Calcula la posición detrás del jugador
        angle = math.radians(player_rotation + 180)  # Opuesto a donde mira
        x = player_pos.x + self.follow_distance * math.sin(angle)
        z = player_pos.z - self.follow_distance * math.cos(angle)

        # Asegura que el bloque esté en el suelo
        return Vec3(x, player_pos.y, z)

    def update_block_position(self, player_pos: Vec3):
        """Actualiza la posición del bloque si el jugador se ha alejado demasiado."""
        distance = self.calculate_distance(player_pos, self.current_pos)

        if distance > self.max_distance:
            # El jugador está demasiado lejos, teletransporta el bloque
            new_pos = self.calculate_position(player_pos)
            self.move_block(new_pos)
            self.current_pos = new_pos

    def calculate_distance(self, pos1: Vec3, pos2: Vec3) -> float:
        """Calcula la distancia horizontal entre dos puntos."""
        return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.z - pos2.z) ** 2)

    def place_block(self, pos: Vec3):
        """Coloca el bloque en la posición especificada."""
        self.mc.setBlock(pos.x, pos.y, pos.z, self.block_id, self.block_data)

    def move_block(self, new_pos: Vec3):
        """Mueve el bloque a una nueva posición."""
        if self.current_pos:
            # Elimina el bloque anterior
            self.mc.setBlock(self.current_pos.x, self.current_pos.y, self.current_pos.z, 0)

        # Coloca el bloque en la nueva posición
        self.place_block(new_pos)
        self.log(f"Bloque movido a: ({new_pos.x:.1f}, {new_pos.y:.1f}, {new_pos.z:.1f})")