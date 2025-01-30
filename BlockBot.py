from typing import Optional
from time import sleep
import random
from MyAdventures.mcpi.vec3 import Vec3
from Agents.BotAgent import BlockAgent


class MinecraftBlockBot:
    """A Minecraft bot that manages a block that follows the player."""

    BLOCK_TYPES = {
        "enderchest": (130, 0, "EnderChest"),
        "craftingtable": (58, 0, "CraftingTable"),
        "furnace": (61, 0, "Furnace"),
        "anvil": (145, 0, "Anvil")
    }

    def __init__(self, bot_name="BlockBot", block_type="enderchest"):
        """
        Initialize the Minecraft block bot.

        Args:
            bot_name (str): Name of the bot
            block_type (str): Type of block to spawn ("enderchest", "craftingtable", "furnace", etc.)
        """
        # Get block information
        block_info = self.BLOCK_TYPES.get(block_type.lower(), self.BLOCK_TYPES["enderchest"])
        block_id, block_data, block_name = block_info

        # Initialize the block machine
        self.agent = BlockAgent(f"{bot_name}_{block_name}", block_id, block_data)
        self.original_name = bot_name
        self.block_name = block_name

        # Set up condition to check player distance
        def block_condition(agent, player_pos: Vec3) -> bool:
            """Determine if the block should be moved."""
            if agent.current_pos is None:
                return True

            distance = agent.calculate_distance(player_pos, agent.current_pos)
            return distance > agent.max_distance or distance < agent.min_distance

        # Set up response to move the block
        def block_response(agent, player_pos: Vec3):
            """Move the block to a new position near the player."""
            new_pos = agent.calculate_position(player_pos)


        # Set condition and response for the agent
        self.agent.set_condition(block_condition)
        self.agent.set_response(block_response)

    def start(self, threaded=True):
        """Start the block bot agent."""
        self.agent.start(threaded)

    def stop(self):
        """Stop the block bot agent."""
        if self.agent.current_pos:
            # Elimina el bloque antes de detener el bot
            self.agent.mc.setBlock(
                self.agent.current_pos.x,
                self.agent.current_pos.y,
                self.agent.current_pos.z,
                0
            )
        self.agent.stop()


def main():
    """Main function to demonstrate block bot usage."""
    global block_bot
    try:
        # Create and start the block bot
        block_type = input(
            "¿Qué tipo de bloque quieres que te siga? (enderchest/craftingtable/furnace/anvil): ").strip()
        if not block_type:
            block_type = "enderchest"

        bot_name = input("¿Qué nombre quieres darle al bot? (Enter para 'BlockBot'): ").strip()
        if not bot_name:
            bot_name = "BlockBot"

        block_bot = MinecraftBlockBot(bot_name, block_type)
        block_bot.start(threaded=True)

        print(f"\nBot iniciado con un {block_type}!")
        print("El bloque te seguirá automáticamente mientras te mueves.")
        print("Presiona Ctrl+C para detener el bot...")

        # Keep the main thread running
        while True:
            sleep(1)

    except KeyboardInterrupt:
        print("\nDeteniendo el Minecraft Block Bot...")
        block_bot.stop()
    except Exception as e:
        print(f"\nError: {e}")
        if 'block_bot' in globals():
            block_bot.stop()


if __name__ == "__main__":
    main()