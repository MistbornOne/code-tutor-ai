#!/bin/bash


# Ask for the host path
echo "Where should I save your conversation logs?"
read -rp "Enter full folder path (or press Enter to use default ~/Documents/conversations/): " LOG_PATH

# Default fallback
LOG_PATH=${LOG_PATH:-$HOME/Documents/conversations/}

# Ensure the folder exists
mkdir -p "$LOG_PATH"

# Run Docker with the bind mount
docker run -it --rm \
  --env-file .env \
  -v "$LOG_PATH":/logs \
  codetutor "$@"

