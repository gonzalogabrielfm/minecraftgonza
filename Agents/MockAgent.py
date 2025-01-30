from Agents.ChatAgent import ChatAgent


class MockAgent(ChatAgent):
    def __init__(self, name: str = "MockBot"):
        super().__init__(name)
        self.set_condition(self.should_mock)
        self.set_response(self.mock_message)

    def should_mock(self, agent, event) -> bool:
        # No mockear los mensajes del propio bot para evitar loops infinitos
        return not event.message.startswith(f"<{self.name}>")

    def mock_message(self, agent, event):
        # Obtener el mensaje original
        original_message = event.message

        # Si el mensaje viene con formato <Player> mensaje, extraer solo el mensaje
        if original_message.startswith("<") and ">" in original_message:
            original_message = original_message.split(">", 1)[1].strip()
        filtered_message = ''.join(filter(lambda c: c.isalpha() or c.isspace(), original_message))

        # Usar map para reemplazar cada caracter
        def mock_char(c: str) -> str:
            # Lista de vocales a reemplazar (incluyendo mayúsculas y minúsculas)
            vowels = 'aeiouAEIOU'
            # Si es vocal minúscula, reemplazar por 'i'
            # Si es vocal mayúscula, reemplazar por 'I'
            return 'I' if c in 'ÀAÁÈEÉÌIÍÒOÓÙUÚ' else 'i' if c in 'àaáèeéìiíòoóùuú' else c

        # Aplicar la transformación y unir los caracteres
        mocked_message = ''.join(map(mock_char, filtered_message))

        # Añadir un "!" al final si no hay uno
        if not mocked_message.endswith("!"):
            mocked_message += "!"

        # Enviar el mensaje mockeado al chat
        self.post_chat(mocked_message)
