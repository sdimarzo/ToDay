import discord
from discord.ext import commands
from operator import attrgetter
import json

from helpers.gif_api import get_rand_gif
from helpers.print_list import print_list
from Task import Task


f = open("config.json")
config = json.load(f)

TOKEN = config["token"]
API_KEY = config["api-key"]
COMMAND_PREFIX = config["command-prefix"]

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix=COMMAND_PREFIX)

task_list = []

@client.command()

async def clean(ctx):
    if len(task_list) == 0:
        await ctx.send("The task list is already empty!")
    else:
        del task_list[:]

@client.command()

async def new_task(ctx, *, message):
    tmp = Task(message, False)
    task_list.append(tmp)
    await ctx.send(
        f"'**{message}**' has been successfully added to the task list!")
@client.command()

async def delete_task(ctx, index: int):
    if len(task_list) == 0:
        await ctx.send(
            "The task list is empty! Create a new " \
            "task by typing: '!new_task <your-new-task>'") 
    else:
        if index > len(task_list) or index <= 0:
            await ctx.send(
                "The task that you tried to " \
                "delete is not present in the task list.\n"\
                "**CORRECT SYNTAX:** '!delete <task-id>'")
        else:
            await ctx.send(
                f"'**{task_list[index-1].content}**' has been successfully " \
                "removed from the task list!")
            task_list.pop(index-1)

@client.command()

async def completed(ctx, index: int):
    if len(task_list) == 0:
        await ctx.send(
            "The task list is empty! Create a new " \
            "task by typing: '!new_task <your-new-task>'")
    else:
        if index > len(task_list) or index <= 0:
            await ctx.send(
                "The task that you tried to " \
                "mark as completed is not present in the task list."\
                "**CORRECT SYNTAX:** '!completed <task-id>")
        else:
            if (task_list[index-1].completed == True):
                await ctx.send(
                    f"'**{task_list[index-1].content}**' has been " \
                    "already completed")
            else:
                task_list[index-1].completed = True
                embed = discord.Embed(title="")
                embed.set_image(
                    url=get_rand_gif(
                        "congrats", 
                        API_KEY, 
                        50))

                await ctx.send(
                    f"{ctx.author.mention} completed " \
                    f"'**{task_list[index-1].content}**'!")
                await ctx.send(embed=embed)

@client.command()

async def print(ctx):
    if len(task_list) == 0:
        await ctx.send(
            "The task list is empty! Create a " \
            "new task by typing: '!new-task <your-new-task>'")
    else:
        await ctx.send(embed=print_list(task_list))

@client.command()

async def modify_task(ctx, index: int, new_task: str):
    if len(task_list) == 0:
        await ctx.send(
            "The task list is empty! Create a new " \
            "task by typing: '!new_task <your-new-task>'")
    else:
        if index > len(task_list) or index <= 0:
            await ctx.send(
                "The task that you tried to " \
                "modify is not present in the task list.\n" \
                "**CORRECT SYNTAX:** '!completed <task-id>'")
        else:
            await ctx.send(
                f"'**{task_list[index-1].content}**' " \
                "has been successfully modified!\n" \
                f"New task: **{new_task}**")
            task_list[index-1].content = new_task

@client.command()

async def command_list(ctx):
    embed = discord.Embed(title="COMMAND LIST", color=discord.Color.red())
    embed.add_field(
        name="!new_task <your-new-task>", 
        value="adds a new task to the task list", inline=False)
    embed.add_field(
        name="!delete <task-id>",
        value="deletes the selected task from the task list", inline=False)
    embed.add_field(
            name="!completed <task-id>",
            value="marks the selected task as completed", inline=False)
    embed.add_field(
            name="!clean", value="removes all the tasks from the task list", 
            inline=False)
    embed.add_field(
            name="!modify_task <task-id> <your-new-task>",
            value="replace the selected task with a new one", inline=False)

    await ctx.send(embed=embed)

@new_task.error

async def new_task_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Something went wrong! You forgot to type the task.\n" \
            "**CORRECT SYNTAX:** '!new_task <your-new-task>'")         

@delete_task.error

async def delete_task_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(
            "Something went wrong! The task-id requested was not " \
            "an integer.\n **CORRECT SYNTAX:** '!delete_task <task-id>'")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Something went wrong! You forgot to type the task-id " \
            "of the task that you want to delete.\n **CORRECT SYNTAX:** " \
            "'!delete_task <task-id>'")

@modify_task.error
async def modify_task_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Something went wrong! You forgot one of the " \
            "parameters.\n **CORRECT SYNTAX:** '!modify_task <task-id> "\
            "<your-new-task>'")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Something went wrong!One of the parameters type was " \
            "now correct.\n **CORRECT SYNTAX:** '!modify_task <task-id> " \
            "<your-new-task>'")

@completed.error
async def completed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Something went wrong! You forgot to type the task-id " \
            "of the task that you want to mark as completed." \
            "**CORRECT SYNTAX:** '!completed <task-id>'")

client.run(TOKEN)