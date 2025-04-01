import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from dathost_api import DathostAPI
from functools import wraps
from typing import Callable

# Debug information
print(f"Current working directory: {os.getcwd()}")
print(f"Looking for .env file in: {os.path.abspath('.env')}")

# Load environment variables
load_dotenv(verbose=True)  # Add verbose=True to see more details

prac_server_id = "67dc83cf3e825ed3401c192f"

token = os.getenv('DISCORD_TOKEN')
print(f"Token being used: {token}")

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # We need this for command handling
# intents.members = True        # Comment out if you don't need member events
# intents.presences = True      # Comment out if you don't need presence updates
bot = commands.Bot(command_prefix='!', intents=intents)
dathost = DathostAPI()

# Add after the imports
allowed_channels = set(map(int, os.getenv('ALLOWED_CHANNELS', '').split(',')))

def check_channel():
    """Decorator to check if command is used in an allowed channel"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            if not allowed_channels:
                # If no channels are configured, allow command everywhere
                return await func(ctx, *args, **kwargs)
            
            if ctx.channel.id not in allowed_channels:
                # Show both channel mention and ID
                current_channel = ctx.channel.mention
                channel_id = ctx.channel.id
                await ctx.send(f"❌ This command cannot be used in {current_channel} (ID: {channel_id})")
                return
            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
@check_channel()
async def servers(ctx):
    """List all servers in the Dathost account"""
    try:
        servers = await dathost.get_servers()
        if not servers:
            await ctx.send("No servers found.")
            return

        chunks = []
        current_chunk = "**🎮 Available Servers:**\n\n"
        
        for server in servers:
            status = "🟢 Online" if server.get('on') else "🔴 Offline"
            players = f"{server.get('players_current', 0)}/{server.get('players_max', 0)}"
            
            domain = server.get('custom_domain', 'N/A')
            game_port = server.get('ports', {}).get('game', 'N/A')
            connect_cmd = f"connect {domain}:{game_port}" if domain != 'N/A' and game_port != 'N/A' else 'N/A'
            
            server_info = (
                f"**{server['name']}**\n"
                f"• Status: {status}\n"
                f"• Players: {players}\n"
                f"• Connect: `{connect_cmd}`\n"
                f"• Location: {server.get('location', 'N/A')}\n\n"
            )
            
            if len(current_chunk) + len(server_info) > 1900:
                chunks.append(current_chunk)
                current_chunk = server_info
            else:
                current_chunk += server_info
        
        if current_chunk:
            chunks.append(current_chunk)
            
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                chunk += f"\nPage {i+1}/{len(chunks)}"
            await ctx.send(chunk)
            
    except Exception as e:
        await ctx.send(f"❌ Error fetching servers: {str(e)}")

# Add these helper functions after the imports and before the commands
async def find_server_by_name(dathost, name: str):
    """Find a server by name (case-insensitive)"""
    servers = await dathost.get_servers()
    return next(
        (s for s in servers if s['name'].lower() == name.lower()),
        None
    )

async def find_server_by_partial_name(dathost, partial_name: str):
    """Find a server by partial name match (case-insensitive)"""
    servers = await dathost.get_servers()
    matches = [s for s in servers if partial_name.lower() in s['name'].lower()]
    return matches

# Update these commands to use names instead of IDs
@bot.command()
@check_channel()
async def start(ctx, *, name: str):
    """Start a server by name"""
    try:
        server = await find_server_by_name(dathost, name)
        if not server:
            # Try partial match if exact match fails
            matches = await find_server_by_partial_name(dathost, name)
            if len(matches) == 0:
                await ctx.send(f"❌ No server found with name: {name}")
                return
            elif len(matches) > 1:
                names = "\n".join(f"• {s['name']}" for s in matches)
                await ctx.send(f"❓ Multiple servers found. Please be more specific:\n{names}")
                return
            server = matches[0]

        success = await dathost.start_server(server['id'])
        if success:
            # Get updated server info
            server = await dathost.get_server_info(server['id'])
            domain = server.get('custom_domain', 'N/A')
            game_port = server.get('ports', {}).get('game', 'N/A')
            connect_cmd = f"connect {domain}:{game_port}" if domain != 'N/A' and game_port != 'N/A' else 'N/A'
            
            await ctx.send(
                f"✅ Server **{server['name']}** has been started!\n\n"
                f"• Connect: `{connect_cmd}`"
            )
        else:
            await ctx.send(f"❌ Failed to start server **{server['name']}**")
    except Exception as e:
        await ctx.send(f"❌ Error starting server: {str(e)}")

@bot.command()
@check_channel()
async def stop(ctx, *, name: str):
    """Stop a server by name"""
    try:
        server = await find_server_by_name(dathost, name)
        if not server:
            # Try partial match if exact match fails
            matches = await find_server_by_partial_name(dathost, name)
            if len(matches) == 0:
                await ctx.send(f"❌ No server found with name: {name}")
                return
            elif len(matches) > 1:
                names = "\n".join(f"• {s['name']}" for s in matches)
                await ctx.send(f"❓ Multiple servers found. Please be more specific:\n{names}")
                return
            server = matches[0]

        success = await dathost.stop_server(server['id'])
        if success:
            await ctx.send(f"✅ Server **{server['name']}** has been stopped!")
        else:
            await ctx.send(f"❌ Failed to stop server **{server['name']}**")
    except Exception as e:
        await ctx.send(f"❌ Error stopping server: {str(e)}")

@bot.command()
@check_channel()
async def restart(ctx, *, name: str):
    """Restart a server by name"""
    try:
        server = await find_server_by_name(dathost, name)
        if not server:
            # Try partial match if exact match fails
            matches = await find_server_by_partial_name(dathost, name)
            if len(matches) == 0:
                await ctx.send(f"❌ No server found with name: {name}")
                return
            elif len(matches) > 1:
                names = "\n".join(f"• {s['name']}" for s in matches)
                await ctx.send(f"❓ Multiple servers found. Please be more specific:\n{names}")
                return
            server = matches[0]

        success = await dathost.restart_server(server['id'])
        if success:
            await ctx.send(f"✅ Server **{server['name']}** has been restarted!")
        else:
            await ctx.send(f"❌ Failed to restart server **{server['name']}**")
    except Exception as e:
        await ctx.send(f"❌ Error restarting server: {str(e)}")

@bot.command()
@check_channel()
async def status(ctx):
    """Show all running servers and their connection details"""
    try:
        servers = await dathost.get_servers()
        running_servers = [s for s in servers if s.get('on')]
        
        if not running_servers:
            await ctx.send("🔴 No servers are currently running.")
            return

        response = "**🟢 Running Servers:**\n\n"
        for server in running_servers:
            domain = server.get('custom_domain', 'N/A')
            game_port = server.get('ports', {}).get('game', 'N/A')
            players = f"{server.get('players_current', 0)}/{server.get('players_max', 0)}"
            connect_cmd = f"connect {domain}:{game_port}" if domain != 'N/A' and game_port != 'N/A' else 'N/A'
            
            response += (
                f"**{server['name']}**\n"
                f"• Players: {players}\n"
                f"• Connect: `{connect_cmd}`\n"
                f"• Map: {server.get('map', 'N/A')}\n\n"
            )

        await ctx.send(response)
        
    except Exception as e:
        await ctx.send(f"❌ Error fetching server status: {str(e)}")

#@bot.command()
@check_channel()
async def debug_server(ctx):
    """Debug command to show raw server data"""
    try:
        servers = await dathost.get_servers()
        if not servers:
            await ctx.send("No servers found.")
            return

        for server in servers:
            # Convert server dict to formatted string
            server_data = "\n".join(f"• {k}: {v}" for k, v in server.items())
            
            # Split into chunks if too long
            chunks = [server_data[i:i+1900] for i in range(0, len(server_data), 1900)]
            
            await ctx.send(f"**Raw Server Data:**\n```\n{chunks[0]}\n```")
            for chunk in chunks[1:]:
                await ctx.send(f"```\n{chunk}\n```")
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@check_channel()
async def prac(ctx):
    """Deprecated command to start the practice server"""
    
    await ctx.send("Noniin focus! Servu on jo päällä!")

    """Get connect info for the Tenet server"""
    try:
        # Find server with 'tenet' in the name
        matches = await find_server_by_partial_name(dathost, 'tenet')
        
        if not matches:
            await ctx.send("❌ No Tenet server found")
            return
            
        server = matches[0]  # Get first match
        
        # Get connection details
        domain = server.get('custom_domain', 'N/A')
        game_port = server.get('ports', {}).get('game', 'N/A')
        players = f"{server.get('players_current', 0)}/{server.get('players_max', 0)}"
        connect_cmd = f"connect {domain}:{game_port}" if domain != 'N/A' and game_port != 'N/A' else 'N/A'
        status = "🟢 Online" if server.get('on') else "🔴 Offline"
        
        response = (
            f"**{server['name']}**\n"
            f"• Status: {status}\n"
            f"• Players: {players}\n" 
            f"• Connect: `{connect_cmd}`\n"
            f"• Map: {server.get('map', 'N/A')}\n"
        )
        
        await ctx.send(response)
        
    except Exception as e:
        await ctx.send(f"❌ Error getting Tenet server info: {str(e)}")
            


# Run the bot
if __name__ == "__main__":
    if not token:
        raise ValueError("No token found in environment variables!")
    bot.run(token) 