import discord
from discord import app_commands 
from itertools import cycle
import wikipedia
import time
import pafy
import random
import os
import json
from discord import FFmpegPCMAudio
import pyaudio
import asyncio
from discord.ext import tasks
from ewmh import EWMH
import yt_dlp
from pytube import YouTube
import functools
import typing
from youtubesearchpython import VideosSearch,ResultMode
import requests

def np():
    try:
        window_manager_manager = EWMH()
        client_list = window_manager_manager.getClientList()

        for window in client_list:
            if '.mp3' in str(window_manager_manager.getWmName(window)):
                return str(window_manager_manager.getWmName(window),encoding='ascii',errors='replace')
    except:
        return

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced
            print('asdf') 
            await tree.sync() #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")
        statusloop.start()
client = aclient()
tree = app_commands.CommandTree(client)

@tasks.loop()
async def statusloop():
    await client.wait_until_ready()
    wname=np()
    if wname !=None:
        await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f' {wname.split(".mp3")[0]}'))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f'on {len(client.voice_clients)} channels'))
    else:
        await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f'Hazırlık maçına'))
    await asyncio.sleep(10)
    
    
        
@tree.command(name = 'cm', description='( ͡° ͜ʖ ͡°)') #guild specific slash command
async def cm(interaction: discord.Interaction):
    cm=random.randint(-13, 31)
    msgmid="="*cm
    embed = discord.Embed(title=f"{interaction.user.nick}'s D :flushed:", description="", colour=discord.Colour.purple())
    embed.description += f"\n"
    if cm < 25:
        embed.description += f"{cm} cm\n"
    else:
        embed.description +=f'{cm} cm    Damn Daniel :flushed: \n'
    embed.description +=f'8{msgmid}D'
    await interaction.response.send_message(embed=embed, ephemeral = False)
    
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@tree.command(name = 'wiki', description='wiki') #guild specific slash command
async def wiki(interaction: discord.Interaction):
        url = 'https://opentdb.com/api.php?amount=1'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            trivia = data['results'][0]['question']
            await interaction.response.send_message(trivia, ephemeral = False)
        except requests.exceptions.RequestException as e:
            print(e)
            await interaction.response.send_message('An error occured while getting question :/', ephemeral = False)
            
            
@tree.command(name = 'control', description='( ͡° ͜ʖ ͡°)') #guild specific slash command
async def control(interaction: discord.Interaction):
    cm=random.randint(1, 2)
    embed = discord.Embed(title=f"{interaction.user.nick}'s D :flushed:", description="", colour=discord.Colour.purple())
    embed.description += f"\n"
    if cm ==2:
        embed.description += f"Kalkık :flushed:\n"
    else:
        embed.description += f"İnik :cry:\n"
    await interaction.response.send_message(embed=embed, ephemeral = False)

@tree.command(name = 'obj', description='random object') #guild specific slash command
async def obj(interaction: discord.Interaction):
    path = "items"
    dir_list = os.listdir(path)
    rand=random.randint(0,4542)
    objj=dir_list[rand]
    await interaction.response.send_message(file=discord.File(f'items/{objj}'), ephemeral = False)
    
@tree.command(name = 'np', description='now playing') #guild specific slash command
async def obj(interaction: discord.Interaction):
    wname=np()
    if wname !=None:
        await interaction.response.send_message(wname.split(".mp3")[0], ephemeral = False)
    else:
        await interaction.response.send_message('Error while getting information of current song :/', ephemeral = False)
@tree.command(name = 'join', description='joins voice channel') #guild specific slash command
async def obj(interaction: discord.Interaction):
    if (interaction.user.voice): 
        channel = interaction.user.voice.channel
        voice = await channel.connect()
        await interaction.response.send_message("Connected!",ephemeral=True)
        voice.play(discord.FFmpegPCMAudio('intro.wav'),after=lambda e:voice.play(PyAudioPCM(), after=lambda e: print(f'Player error: {e}') if e else None))
        while True:
            if len(channel.members)<2:
                voice.stop()
                await asyncio.sleep(1)
                await voice.disconnect()
                break
            await asyncio.sleep(120)
    else:
        await interaction.response.send_message("You are not in a voice channel",ephemeral=True)

@tree.command(name = 'disconnect', description='disconnects from voice channel') #guild specific slash command
async def obj(interaction: discord.Interaction):
    if (interaction.guild.voice_client): 
        interaction.guild.voice_client.stop()
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Disconnected!",ephemeral=True)
    else:
        await interaction.response.send_message("You are not in a voice channel",ephemeral=True)
        
        
@tree.command(name = 'download', description='downloads given song to specific radio') #guild specific slash command
@app_commands.describe(categories='Select the category')
@app_commands.choices(categories=[
    discord.app_commands.Choice(name='2000',value=1),
    discord.app_commands.Choice(name='Wave',value=2),
    discord.app_commands.Choice(name='Phonk',value=3),
    discord.app_commands.Choice(name='Hardstyle',value=4),
    discord.app_commands.Choice(name='Techno',value=5),
    discord.app_commands.Choice(name='Drum & Bass',value=6),
    discord.app_commands.Choice(name='Rock & Metal',value=7)
    ])
async def downloader(interaction: discord.Interaction, categories: discord.app_commands.Choice[int],song: str):
    if 'https://' in song:
        await interaction.response.send_message(f'Downloading Song: {YouTube(song).title} - Category: {categories.name} ')
        await download(url=song,category=categories.name)
        msg=await interaction.original_response()
        return await msg.add_reaction('👍')
    else:
        await interaction.response.send_message(f'Please wait while I search for {song}')
        result = await search_song(song)
        if result:
            embed = discord.Embed(title=f"",description="", colour=discord.Colour.random())
            embed.description += '1- ' + YouTube(result[0]).title +'\n'
            embed.description += '2- ' + YouTube(result[1]).title +'\n'
            embed.description += '3- ' + YouTube(result[2]).title +'\n'
            embed.description += '4- ' + YouTube(result[3]).title +'\n'
            embed.description += '5- ' + YouTube(result[4]).title +'\n\n'
            embed.description+='You have 60 seconds to select from reactions.'
            await interaction.edit_original_response(embed=embed,content=f'Search results for {song} {interaction.user.mention}')
            emotes=['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
            msg=await interaction.original_response()
            for i in emotes:
                await msg.add_reaction(i)
            cache_msg = discord.utils.get(client.cached_messages, id=msg.id)
            for i in range(30):
                await asyncio.sleep(2)
                for i in range(5):
                    if cache_msg.reactions[i].count>1:
                        await cache_msg.clear_reactions()
                        await interaction.edit_original_response(embed=None,content=f'Downloading Song: {YouTube(result[i]).title} - Category: {categories.name}')
                        await download(url=YouTube(result[i]).watch_url,category=categories.name)
                        msg=await interaction.original_response()
                        return await msg.add_reaction('👍')
            await cache_msg.clear_reactions()
            return await interaction.edit_original_response(embed=None,content=f'User interaction timed out ⏰')
        else:
            return await interaction.edit_original_response(embed=None,content=f'An error occured while searching for the song, please try again with song link')

        

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def search_song(song):

    playlistsSearch = VideosSearch(song, limit = 10)
    if len(playlistsSearch.result()['result'])>=5:
        return [playlistsSearch.result()['result'][i]['link'] for i in range(5)]
    else:
        return None
    
@to_thread
def download(url,category):
        try:
            with yt_dlp.YoutubeDL({"format": "bestaudio","cookiefile":"cookies.txt", "quiet": False,'outtmpl': f'Categories/{category}/%(title)s.%(ext)s',"no_warnings": True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}) as ydl:
                ydl.download([url])
        except:
            pass

class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)

    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)
client.run('MTA3OTEyMjEwMjQyMDAwMDg2MA.GJklz6.m6dddyyCAAEgCMG2ovSvnaFdxeGM9-xVe74rK8')
