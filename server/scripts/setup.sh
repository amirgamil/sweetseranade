#!/bin/zsh
# This is used for coloring output of this script
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Running Setup Script"

# Notify the user if an OpenAI key is not detected
if [[ -z "${OPENAI_API_KEY}" ]]; then
  echo -e "${RED}OPENAI_API_KEY was not detected in environment variable. Please ensure it's located in .env${NC}"
fi

# Install the punkt file for nltk 
poetry run python <<HEREDOC
import nltk
nltk.download('punkt')
print('here')
HEREDOC

echo -e "${GREEN}Shell Script Done${NC}"
exit 0
