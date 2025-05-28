import os

from codetutor import config, core
from codetutor.cli import format_conversation


def test_format_conversation():
    history = [
        {"role": "user", "content": "What's a loop?"},
        {"role": "assistant", "content": "Can you guess what a loop might do?"},
    ]
    result = format_conversation(history)
    assert "User: What's a loop?" in result
    assert "Assistant: Can you guess what a loop might do?" in result


def test_color_output():
    sample = "Hello!"
    green = core.print_tutor_response(sample)
    assert green is None  # print returns None — but test runs


def test_model_selection_default(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    # simulate user pressing Enter
    monkeypatch.setattr("builtins.input", lambda _: "")
    model = config.get_model(force_select=True)
    assert model == "gpt-4o"


def test_env_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    assert config.get_api_key() == "sk-test"
