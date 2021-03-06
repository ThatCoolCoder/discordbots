import os
import time

from better_profanity import profanity
profanity.load_censor_words()
profanity.add_censor_words(['play', 'dad'])

from common import run_bot
from abstract_bot import Bot

class PauseBot(Bot):
    # Stupid joke bot that says "Pause" if it detects anyone saying sexual things but only those involving men
    ANTI_CENSOR_WORDS = ['woman', 'female', 'girl', 'lady']

    def __init__(self, token: str):
        super().__init__(token)

    async def on_ready(self):
        pass

    async def on_message(self, message):
        if message.author != self.user:
            if not any([word in message.content for word in self.ANTI_CENSOR_WORDS]):    
                if profanity.contains_profanity(message.content):
                    await message.channel.send(':pause_button:   Pause bro')

if __name__ == '__main__':
    run_bot(PauseBot)