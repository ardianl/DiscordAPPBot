import discord
from discord.ext import commands
from discord import app_commands
from subprocess import run as Subrun
import pygetwindow as gw

serverRunning = False
ServerID = 'ENTER SERVER ID HERE'    #DEV SERVER ID
#ServerID = 'ENTER SERVER ID HERE' #PROD SERVER ID
Token = 'ENTER TOKEN HERE'
intents = discord.Intents.default()
intents.message_content =True
GUILD_ID = discord.Object(id=ServerID)

print('Starting...')
# SET UP BOT TO SERVER
class Client(commands.Bot):
        async def on_ready(self):
                print(f'Running...')
                try: # SYNC BOT COMMANDS TO SERVER
                        guild = discord.Object(id=ServerID)
                        synced = await self.tree.sync(guild=guild)
                        print(f'Synced {len(synced)} commands to guild {guild.id}')
                except Exception as e:
                        print(f'Error syncing commands: {e}')
                print(f'Logged on as {self.user}!')
# CREATE CLIENT TO ATTACH COMMANDS
client = Client(command_prefix='!', intents=intents)
# CREATE ALL THE SLASH COMMANDS
@client.tree.command(name='pal-start', description='Starts Palworld server', guild=GUILD_ID)
async def startServer(interaction: discord.Interaction):
        global serverRunning
        print(f'Startup command received.')
        if serverRunning:
                print(f'IGNORED')
                await interaction.response.send_message(content='SERVER ALREADY RUNNING', ephemeral=True)
        else:
                await interaction.response.send_message(content='Starting server...', ephemeral=True)
                serverRunning = True
                Subrun(['start', 'steam://run/2394010'], shell=True) # LAUNCH PALWORLD DEDICATED SERVER THROUGH STEAM APP ID

@client.tree.command(name='pal-stop', description='Stops Palworld server', guild=GUILD_ID)
async def stopServer(interaction: discord.Interaction):
        global serverRunning
        print(f'Stop command received.')
        if serverRunning:
                await interaction.response.send_message(content='Closing palworld server', ephemeral=True)
                serverRunning = False
                find_and_kill_window('PalServer-Win64-Shipping-Cmd') # FIND AND CLOSE SERVER WINODW
        else:
                print(f'IGNORED')
                await interaction.response.send_message(content='SERVER NOT RUNNING', ephemeral=True)
        
@client.tree.command(name='pal-abort', description='Abort computer shutdown', guild=GUILD_ID)
async def abortShutdown(interaction: discord.Interaction):
        print(f'Abort command received.')
        await interaction.response.send_message(content='Aborting computer shutdown', ephemeral=True)
        Subrun('shutdown /a', shell=True) # ABORT SHUTDOWN

@client.tree.command(name='pal-shutdown', description='Turns off bot PC', guild=GUILD_ID)
async def shutdownPC(interaction: discord.Interaction):
        global serverRunning
        print(f'Shutdown command received.')
        await interaction.response.send_message(content='Closing server; PC shutdown in 60 seconds', ephemeral=True)
        if not serverRunning:
                print(f'IGNORED')
        serverRunning = False
        find_and_kill_window('PalServer-Win64-Shipping-Cmd')
        Subrun('shutdown /s /t 60', shell=True) # 60 SECONDS SHUTDOWN TIEMR

@client.tree.command(name='pal-disconnect', description='Disconnects bot', guild=GUILD_ID)
async def disconnectBot(interaction: discord.Interaction):
        print(f'Disconnect command received.')
        await interaction.response.send_message(content='Disconnecting bot', ephemeral=True)
        await client.close() # CLOSE BOT CLIENT

# DEFINE FUNCTIONS
def find_and_kill_window(window_title: str):
        try:
                targetWindow = gw.getWindowsWithTitle(window_title)[0]
                targetWindow.close()
        except Exception as e:
                pass

# START BOT
client.run(Token)

#CLIENT SESSION ENDED
# print(f'Shutting down!')
# Subrun('shutdown /s /t 60', shell=True)