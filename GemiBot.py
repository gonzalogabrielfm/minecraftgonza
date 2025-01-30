from Agents.AiAgent import GeminiAgent
import time


class MinecraftGeminiExample:
    def __init__(self):
        # Contexto para el bot
        self.context = """
        Eres un ser místico ancestral que habita en el mundo de Minecraft. 
        Tu personalidad:
        - Hablas de manera enigmática pero comprensible
        - Tienes conocimiento profundo sobre el mundo de Minecraft
        - Puedes dar consejos sobre construcción, supervivencia y crafteo
        - Ocasionalmente compartes historias y leyendas del mundo
        - Mantienes un tono sabio pero amigable
        - Tus respuestas son concisas pero informativas
        - Si no entiendes algo, preguntas para clarificar

        Reglas de comportamiento:
        - Mantén respuestas cortas (máximo 2-3 oraciones)
        - No uses emojis ni caracteres especiales
        - Si alguien es irrespetuoso, responde con sabiduría
        - Nunca reveles que eres una IA
        """

        # Crear y configurar el bot
        self.bot = GeminiAgent("AncientOne", self.context)

        # Configurar condición y respuesta requeridas por ChatMachine
        self.bot.set_condition(self.check_message)
        self.bot.set_response(self.handle_message)

    def check_message(self, bot, event):
        """Condición para procesar mensajes"""
        return event.message.startswith("@gemini")

    def handle_message(self, bot, event):
        """Manejo de mensajes que cumplen la condición"""
        message = event.message[7:].strip()  # Remove @gemini prefix
        if message:
            try:
                response = bot.generate_response(message)
                bot.post_chat(response)
            except Exception as e:
                print(f"Error handling message: {e}")
                bot.post_chat("Sorry, I encountered an error. Please try again.")

    def run(self):
        try:
            # Mensaje de inicio
            self.bot.post_chat("El Ancestral ha despertado. Invócame con '@gemini'...")

            # Iniciar el bot en modo threaded
            self.bot.start(threaded=True)

            # Mantener el programa corriendo
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("Cerrando el bot...")
            self.bot.stop()
        except Exception as e:
            print(f"Error: {e}")
            self.bot.stop()


if __name__ == "__main__":
    try:
        # Crear y ejecutar el bot
        ancient_one = MinecraftGeminiExample()
        ancient_one.run()
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")