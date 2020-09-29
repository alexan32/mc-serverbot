# Description: handless discord server access the 'mc-instance-manager' lambda.
# 
# Last Update: Seth Alexander 7/30/2020. added start, stop, ip commands. added
# invokeManager function.

import discord
import boto3
import json

from botocore.exceptions import ClientError
from discord.ext import commands


# setup ----------------------------------------
with open("config.json") as f:
    config = json.load(f)

lambdaClient = boto3.client(
    'lambda', 
    aws_access_key_id=config['access_key'],
    aws_secret_access_key=config['secret_key'],
    region_name=config['region']
)
bot = commands.Bot(command_prefix = "!")
lambdaName = "mc-instance-manager"
currentPlayers = 0

# functions ------------------------------------
def invokeManager(payload):

    try:
        response = lambdaClient.invoke(
            FunctionName=lambdaName,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )
        body = json.loads(response['Payload'].read().decode("utf-8"))
    except ClientError as e:
        errorString = f"Bot failed to call the server manager. Please find the nearest karen and give her this: {e['Error']}"
        body = {"success": False, "message": errorString, "body": {}}
        print(e)
    return body

# events ---------------------------------------
@bot.event
async def on_ready():
    print("bot is ready")

# @bot.command()
# async def playerCount(ctx):
#     await ctx.send(f"current players: {currentPlayers}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"```My ping is {str(round(bot.latency * 1000))}ms```")

@bot.command()
async def start(ctx):
    response = invokeManager({"op":"start"})
    print(response)
    await ctx.send(f"```{response['message']}```")

@bot.command()
async def stop(ctx):
    response = invokeManager({"op":"stop"})
    print(response)
    await ctx.send(f"```{response['message']}```")

@bot.command()
async def ip(ctx):
    response = invokeManager({"op":"ip"})
    print(response)
    await ctx.send(f"```{response['message']}```")

@bot.command(aliases=['state'])
async def getState(ctx):
    response = invokeManager({"op": "getState"})
    print(response)
    await ctx.send(f"```{response['message']}```")
    

# execution ------------------------------------
if __name__ == "__main__":
    bot.run(config['discord_token'])