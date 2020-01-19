from profanity_check import predict, predict_prob
import re
import discord

def get_prob(message):
    '''
    Parameter (Discord Message): the discord message the bot has recieved

    Returns (float): a float value represent the probability profanity is the message
    '''
    #use .content to get the string in the Discord message and the wrap it in a list
    #get the probability from the first value in the numpy array then convert it into a native python float using .item()
    return predict_prob([message.content])[0].item()

def parse_question(message):
    '''
    Parameter (Discord Message): the discord message the bot has recieved

    Return (dict): dictionary containing all of the information gathered from parsing the message
        
    Return (None): return nothing if the channel is detected to not be a dmchannel
    '''
    #the message author
    user = message.author
    #the message content
    message_content = message.content
    #the profanity check
    profanity_prob = get_prob(message)
    #return the full bot message
    bot_message = {
        "author": user,
        "content": message_content,
        "profanity_check": profanity_prob
    }
    return bot_message

def parse_command_permit(message):
    '''
    Parameter (Discord Message): the discord message the bot has recieved

    Return (boolean): returns true if the message is a proper permit command
    '''
    command_matcher = re.compile("^!permit \#[0-9]+$")
    match = command_matcher.fullmatch(message.content)
    if match:
        return True
    else:
        return False 

def parse_command_reject(message):
    '''
    Parameter (Discord Message): the discord message the bot has recieved

    Return (boolean): returns true if the message is a proper permit command
    '''
    command_matcher = re.compile("^!reject \#[0-9]+$")
    match = command_matcher.fullmatch(message.content)
    if match:
        return True
    else:
        return False 

def create_permit_embed_private(question):
    '''
    Parameter question (dict): the dictionary containing all of the information from the question

    Return (Discord Embed): the permit embed to be posted for the moderators to see
    '''
    result_embed = discord.Embed() 
    result_embed.set_footer(text="type \"!permit #{insert valid id}\" or \"!reject #{insert valid id}\"")
    result_embed.set_author(name=str(question["author"]))
    result_embed.add_field(name="Question", value=str(question["content"]), inline=False)
    result_embed.add_field(name="Profanity Check", value=str(question["profanity_check"]), inline=True)
    result_embed.add_field(name="Question #ID", value=str(question["id"]), inline=True)
    return result_embed

def create_permit_embed_public(question):
    '''
    Parameter question (dict): the dictionary containing all of the information from the question

    Return (Discord Embed): the permit embed to be posted for the public discord to see
    '''
    result_embed = discord.Embed() 
    result_embed.set_author(name="DMBot")
    result_embed.add_field(name="Question", value=str(question["content"]), inline=False)
    return result_embed

def get_config_information():
    '''
    Return (dict): the dictionary containing all of the information gathered from the configuration file
    
    Return (None): returns None if the config file is not found
    '''
    try:
        with open("t_config.txt", "r") as conf_text:
            key_path = conf_text.readline()
            #slice the the keypath to make sure there is no newline character
            key_path = key_path[0:len(key_path)-1]

            guild_name = conf_text.readline()
            guild_name = guild_name[0:len(guild_name)-1]

            review_channel = conf_text.readline()
            review_channel = review_channel[0:len(review_channel)-1]

            question_channel = conf_text.readline()
            question_channel = question_channel[0:len(question_channel)-1]

            conf_dict = {
                "key_path": key_path,
                "guild_name": guild_name,
                "review_channel": review_channel,
                "question_channel": question_channel
            }
            return conf_dict
    except FileNotFoundError:
        return None
        