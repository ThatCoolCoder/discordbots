from copy import deepcopy
import abc # abstract class

import discord
import asyncio

class Bot(abc.ABC):
    client = discord.Client()
    user = None

    class ChannelSettings:
        def __init__(self, default_channel_value):
            self.DEFAULT_CHANNEL_VALUE = deepcopy(default_channel_value)

            self.__settings = {}
        
        def __getitem__(self, channel_id: int):
            if channel_id not in self.__settings:
                self.__settings[channel_id] = deepcopy(self.DEFAULT_CHANNEL_VALUE)
            return self.__settings[channel_id]
        
        def __setitem__(self, channel_id: int, value):
            if channel_id not in self.__settings:
                self.__settings[channel_id] = deepcopy(self.DEFAULT_CHANNEL_VALUE)
            self.__settings[channel_id] = value

    def __init__(self, token, default_channel_settings_value={}):
        self.token = token
        self.channel_settings = self.ChannelSettings(default_channel_settings_value)

        @self.client.event
        async def on_ready():
            await self.__on_ready()
        
        @self.client.event
        async def on_message(message):
            await self.__on_message(message)
        
    def run(self):
        self.client.run(self.token)
    
    async def __on_ready(self):
        print(f'Logged in as {self.client.user}')
        self.user = self.client.user
        await self.on_ready()
    
    @abc.abstractmethod
    async def on_ready(self):
        '''Method to be run when the bot is logged in and ready'''

    async def  __on_message(self, message):
        await self.on_message(message)
    
    @abc.abstractmethod
    async def on_message(self, message):
        '''Method to be run when a message is recieved'''