import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".codetutor"
CONFIG_FILE = CONFIG_DIR / "config"


def _read_config():
    if CONFIG_FILE.exists():
        return dict(
            line.strip().split("=", 1)
            for line in CONFIG_FILE.read_text().splitlines()
            if "=" in line
        )
    return {}


def _write_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = [f"{key}={value}" for key, value in data.items()]
    CONFIG_FILE.write_text("\n".join(lines) + "\n")


def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    raise RuntimeError(
        "❌ OPENAI_API_KEY not set. Please export it or use a .env file."
    )


def get_model(force_select=False):
    config = _read_config()

    if not force_select and "OPENAI_MODEL" in config:
        return config["OPENAI_MODEL"]

    # Prompt user to choose a model
    models = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "o3-mini"]
    print("\nSelect a model:")
    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")

    while True:
        choice = input("Enter model number (default 1): ").strip()
        if choice == "":
            selected_model = models[0]
            break
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            selected_model = models[int(choice) - 1]
            break
        print("Invalid choice. Please try again.")

    # Save choice
    config["OPENAI_MODEL"] = selected_model
    _write_config(config)

    return selected_model


def get_conversation_dir():
    config = _read_config()

    # Auto-detect bind-mounted /logs directory
    if Path("/logs").exists():
        return Path("/logs")

    if "CONVERSATION_DIR" in config and Path(config["CONVERSATION_DIR"]).exists():
        return Path(config["CONVERSATION_DIR"])

    print("\nWhere should I save your conversation logs?")
    default_dir = Path.cwd() / "conversations"
    print(f"Press Enter to use the default: {default_dir}")

    path = input("Enter a folder path: ").strip()
    save_path = Path(path) if path else default_dir
    save_path.mkdir(parents=True, exist_ok=True)

    config["CONVERSATION_DIR"] = str(save_path)
    _write_config(config)

    return save_path
