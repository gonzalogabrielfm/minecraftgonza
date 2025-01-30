from mcpi.minecraft import Minecraft
import random
import time
import threading

# Connect to Minecraft
mc = Minecraft.create()

# List of insults for the bot to use
INSULTS = [
    "Your building skills are as flat as a slime!",
    "Did a creeper design your house?",
    "Even a zombie builds better than you!",
    "Your armor looks like it came from a village discount chest!",
    "Nice inventory... did you get it from a wandering trader?",
    "Your parkour skills remind me of a falling anvil!",
    "I've seen better builds in creative mode!",
    "A skeleton has better aim than you!"
]

def send_insults():
    """Periodically send insults to chat"""
    while True:
        try:
            mc.postToChat(f"ChaosBot: {random.choice(INSULTS)}")
        except:
            print("Failed to send insult")
        time.sleep(5)  # Send insult every 5 seconds

def spawn_tnt():
    """Spawn TNT near players"""
    while True:
        try:
            # Get player position
            pos = mc.player.getTilePos()
            
            # Add random offset
            x = pos.x + random.randint(-2, 2)
            y = pos.y
            z = pos.z + random.randint(-2, 2)
            
            # Place TNT and trigger it
            mc.setBlock(x, y, z, 46)         # Place TNT
            mc.setBlock(x, y-1, z, 152)      # Place redstone block underneath
            
        except:
            print("Failed to spawn TNT")
        
        time.sleep(8)  # Spawn TNT every 8 seconds

print("Starting Chaos Bot...")

# Start insult thread
insult_thread = threading.Thread(target=send_insults)
insult_thread.daemon = True
insult_thread.start()

# Start TNT thread
tnt_thread = threading.Thread(target=spawn_tnt)
tnt_thread.daemon = True
tnt_thread.start()

# Keep running until interrupted
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping bot...")