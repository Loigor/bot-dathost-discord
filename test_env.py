from dotenv import load_dotenv
import os

print("Starting test...")
load_dotenv(verbose=True)
token = os.getenv('DISCORD_TOKEN')
print(f"Token from env: {token}") 