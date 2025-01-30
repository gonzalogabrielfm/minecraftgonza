from Agents.MockAgent import MockAgent
import time

if __name__ == "__main__":
    try:
        # Crear una instancia de MockBot
        mock_bot = MockAgent()

        # Iniciar el bot en un hilo separado
        mock_bot.start(threaded=True)

        print("MockBot está en funcionamiento. Escribe en el chat de Minecraft y observa cómo responde.")

        # Mantener el programa corriendo para que el bot siga escuchando
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Deteniendo MockBot...")
        mock_bot.stop()
