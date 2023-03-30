from io import StringIO
from dotenv import load_dotenv

def parse_env_file(file):
    # Filter out any lines that start with "source denison-ai-api/bin/activate"
    lines = [line for line in file.split("\n") if not line.startswith("source denison-ai-api/bin/activate")]
    # Join the remaining lines and return a StringIO object
    return StringIO("\n".join(lines))

# Load environment variables from .env file, skipping the line that starts with "source denison-ai-api/bin/activate"
load_dotenv(".env", parser=parse_env_file)  # Required to load .env