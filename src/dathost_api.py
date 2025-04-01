import os
import aiohttp
import base64
from dotenv import load_dotenv

class DathostAPI:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://dathost.net/api/0.1"
        self.email = os.getenv('DATHOST_EMAIL')
        self.password = os.getenv('DATHOST_PASSWORD')
        self.auth_header = self._create_auth_header()

    def _create_auth_header(self):
        """Create basic auth header for Dathost API"""
        credentials = f"{self.email}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}

    async def get_account(self):
        """Get account information"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.get(f"{self.base_url}/account") as response:
                return await response.json()

    async def get_servers(self):
        """Get list of all servers"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.get(f"{self.base_url}/game-servers") as response:
                return await response.json()

    async def get_server_info(self, server_id: str):
        """Get information about a specific server"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.get(f"{self.base_url}/game-servers/{server_id}") as response:
                return await response.json()

    async def start_server(self, server_id: str):
        """Start a game server"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.post(f"{self.base_url}/game-servers/{server_id}/start") as response:
                return response.status == 200

    async def stop_server(self, server_id: str):
        """Stop a game server"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.post(f"{self.base_url}/game-servers/{server_id}/stop") as response:
                return response.status == 200

    async def restart_server(self, server_id: str):
        """Restart a game server"""
        async with aiohttp.ClientSession(headers=self.auth_header) as session:
            async with session.post(f"{self.base_url}/game-servers/{server_id}/restart") as response:
                return response.status == 200 