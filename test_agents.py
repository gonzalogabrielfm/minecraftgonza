import pytest
from unittest.mock import MagicMock, patch
from Agents.ChatAgent import ChatAgent
from Agents.BlockAgent import BlockAgent
from Agents.AiAgent import GeminiAgent
from Agents.MockAgent import MockAgent
from MyAdventures.mcpi.vec3 import Vec3
import os

@pytest.fixture
def mock_minecraft():
    """Crea un objeto Minecraft simulado con métodos mockeados."""
    mock_mc = MagicMock()
    mock_mc.events.pollChatPosts.return_value = []
    return mock_mc


def test_chat_agent_initialization():
    agent = ChatAgent("TestChatAgent")
    assert agent.name == "TestChatAgent"
    assert agent.mc is not None


def test_block_agent_initialization():
    agent = BlockAgent("TestBlockAgent", block_id=1)
    assert agent.name == "TestBlockAgent"
    assert agent.block_id == 1


def test_block_agent_follow_logic(mock_minecraft):
    agent = BlockAgent("TestBlockAgent", block_id=1)
    agent.mc = mock_minecraft
    agent.target_player_id = 123
    mock_minecraft.entity.getPos.return_value = (10, 5, 10)

    agent.current_pos = Vec3(8, 5, 8)
    agent.listen()

    assert agent.current_pos is not None


@pytest.fixture
def mock_gemini_agent():
    """Create a mock GeminiAgent with mocked AI response."""
    agent = GeminiAgent("TestGeminiAgent", "Test context")
    agent.model = MagicMock()
    agent.model.generate_content.return_value.text = "AI Response"
    return agent

# Test initialization of GeminiAgent
def test_gemini_agent_initialization(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    agent = GeminiAgent("TestGeminiAgent", "Test context")
    assert agent.name == "TestGeminiAgent"
    assert agent.context == "Test context"

def test_gemini_agent_generate_response(mock_gemini_agent):
    response = mock_gemini_agent.generate_response("Hello")
    assert response == "AI Response"

@patch('os.getenv')
def test_gemini_agent_setup_ai_success(mock_getenv, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    mock_getenv.return_value = "fake_key"

    agent = GeminiAgent("TestGeminiAgent", "Test context")
    agent.setup_ai()

    assert agent.model is not None



def test_gemini_agent_generate_empty_response(mock_gemini_agent):
    mock_gemini_agent.model.generate_content.return_value.text = ""

    with pytest.raises(Exception, match="Empty response from Gemini"):
        mock_gemini_agent.generate_response("Hello")




def test_mock_bot_initialization():
    agent = MockAgent()
    assert agent.name == "MockBot"

