import os
from common import run_bot
from abstract_bot import Bot

class BotBot(Bot):
    '''You'll find that a lot of the 'consts' in this class
    are actually defined in the on_ready() method,
    as they rely upon data that is only available after login
    '''

    CHATBOT_RUNNER_FILE = 'node_chatbot/chatbotRunner.mjs'

    def __init__(self, token:str):
        default_settings = {'activated' : True,'requires_trigger' : True,
            'use_tts' : False}
        super().__init__(token, default_settings)

    
    async def on_ready(self):
        self.RESPONSE_TRIGGER = f'hey {self.user.name}'
        self.CONFIG_KEYWORD = f'${self.user.name}config'
        self.CONFIG_HELP = f'''```
usage: {self.CONFIG_KEYWORD} <argument>
arguments:
activate            allow the bot to talk
deactivate          prevent the bot from talking
require_trigger     only reply when addressed with "{self.RESPONSE_TRIGGER}"
no_require_trigger  reply to all messages in the channel
use_tts             use Discord text-to-speech when sending messages
no_use_tts          do not use text-to-speech when sending messages
help                bring up this help menu
current_config      show what the settings are currently set to
```'''

    async def on_message(self, message):
        if message.author != self.user:
            reply = None

            if message.content.startswith(self.CONFIG_KEYWORD):
                reply = self.process_config_command(
                    message.content[len(self.CONFIG_KEYWORD):],
                    message.channel.id)
                await message.channel.send(reply)
            
            elif self.channel_settings[message.channel.id]['activated']:
                response_trigger_present = False
                clean_content = message.content
                if message.content.lower().startswith(self.RESPONSE_TRIGGER):
                    response_trigger_present = True
                    clean_content = message.content[len(self.RESPONSE_TRIGGER):]
                
                trigger_required = self.channel_settings[message.channel.id]\
                    ['requires_trigger']
                if (not trigger_required) or response_trigger_present:
                    reply = self.create_reply(clean_content)

                use_tts = self.channel_settings[message.channel.id]['use_tts']
                await message.channel.send(reply, tts=use_tts)
        
    def create_reply(self, prompt: str):
        command = f'node {self.CHATBOT_RUNNER_FILE} {self.user.name} {prompt}'
        return os.popen(command).read()
    
    def process_config_command(self, command: str, channel_id: int):
        '''Note that command should not have prefix like $config'''
        sections = command.split(' ')
        this_channel_settings = self.channel_settings[channel_id]
        if 'activate' in sections:
            this_channel_settings['activated'] = True
            return 'I am activated'
        elif 'deactivate' in sections:
            this_channel_settings['activated'] = False
            return 'I am deactivated'
        elif 'require_trigger' in sections:
            this_channel_settings['requires_trigger'] = True
            return f'I will now only respond to messages starting with "{self.RESPONSE_TRIGGER}"'
        elif 'no_require_trigger' in sections:
            this_channel_settings['requires_trigger'] = False
            return 'I will now respond to all messages'
        elif 'use_tts' in sections:
            this_channel_settings['use_tts'] = True
            return 'I will now use text-to-speech when replying'
        elif 'no_use_tts' in sections:
            this_channel_settings['use_tts'] = False
            return 'I will now not use text-to-speech when replying'
        elif 'help' in sections:
            return self.CONFIG_HELP
        elif 'current_config' in sections:
            # First find the longest setting name so we can align the values
            longest_setting_name = 0
            for setting_name in this_channel_settings:
                if len(setting_name) > longest_setting_name:
                    longest_setting_name = len(setting_name)
            target_setting_name_length = longest_setting_name + 1

            setting_str = ''
            for setting_name in this_channel_settings:
                spaces_required = target_setting_name_length - len(setting_name)
                padding = ' ' * spaces_required
                padded_setting_name = f'{setting_name}:{padding}'
                setting_value = this_channel_settings[setting_name]
                setting_str += f'{padded_setting_name}{setting_value}\n'
            setting_str = setting_str[:-1] # trim trailing newline

            return f'''```Current configuration:\n{setting_str}```'''
        else:
            return f'Unrecognised command. Type `{self.CONFIG_KEYWORD} help` for more info.'

if __name__ == '__main__':
    run_bot(BotBot)