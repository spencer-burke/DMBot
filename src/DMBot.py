import discord
import asyncio
from Queue import Queue
from BotUtils import parse_question, create_permit_embed_public, create_permit_embed_private, parse_command_permit, parse_command_reject, get_config_information
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

question_id = 1
question_queue = Queue()

config_data = get_config_information()

class my_client(discord.Client):

    def __init__(self, id, queue):
        super().__init__()
        self.id = id
        self.queue = queue  

    def get_question_channel(self, guild, question_channel):
        '''
        Return (Discord Channel): return the correct discord channel
        '''
        channel = discord.utils.get(self.get_all_channels(), guild__name=guild, name=question_channel)
        return channel

    def get_review_channel(self, guild, review_channel):
        '''
        Return (Discord Channel): return the correct discord channel
        '''
        channel = discord.utils.get(self.get_all_channels(), guild__name=guild, name=review_channel)
        return channel
    
    async def handle_message(self, message):
        if message.author.id == self.user.id:
            return
        #if the message is from a direct message channel it is assumed to be a question and handed over to the moderators
        if message.guild == None:
            question = parse_question(message)
            question["id"] = self.id
            self.queue.enqueue(question)
            self.id += 1
            if self.queue.size() == 1:
                await self.review_channel.send(embed=create_permit_embed_private(self.queue.peek()))
        #if the message is not a direct message it is assumed to be a command
        else:
            if message.channel == self.review_channel:
                if self.queue.size() > 0:
                    #if the message matches a permit command
                    if parse_command_permit(message) == True:
                        command_id = int(message.content[9:])
                        #make sure the id is valid
                        if command_id == self.queue.peek()["id"]:
                            await self.question_channel.send(embed=create_permit_embed_public(self.queue.dequeue()))
                            #if there is another question to be reviewed send that to be reviewed
                            if self.queue.size() > 0:
                                await self.review_channel.send(embed=create_permit_embed_private(self.queue.peek()))
                    #if the message matches a reject command
                    elif parse_command_reject(message) == True:
                        command_id = int(message.content[9:])
                        #make sure the id is valid
                        if command_id == self.queue.peek()["id"]:
                            self.queue.dequeue()
                            await self.review_channel.send("Question with id \#" + str(command_id) + " has been deleted")
                            #if there is another question to be reviewed send that to be reviewed
                            if self.queue.size() > 0:
                                await self.review_channel.send(embed=create_permit_embed_private(self.queue.peek()))

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.review_channel = self.get_review_channel(config_data["guild_name"], config_data["review_channel"])
        self.question_channel = self.get_question_channel(config_data["guild_name"], config_data["question_channel"])

    async def on_message(self, message):
       await self.handle_message(message)

def main():
    client = my_client(question_id, question_queue)

    with open(config_data["key_path"], "r") as file_data:
        BOT_KEY = file_data.readline()
        
    client.run(BOT_KEY)

if __name__ == "__main__":
    main()
