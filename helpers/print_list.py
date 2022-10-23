import discord

def print_list(task_list):
    embed = discord.Embed(title="TO DO:", color=discord.Color.green())
    tasks = ""
    completed = ""
    task_id = ""
    counter = 1
    for x in task_list:
        task_id += f"{str(counter)} \n"
        if x.completed == False:
            completed += ":x: \n"
        else:
            completed += ":white_check_mark: \n"
        tasks += f"{x.content} \n"
        counter += 1
        
    embed.add_field(name ="ID", value=task_id , inline=True)
    embed.add_field(name="STATUS", value=completed, inline=True)
    embed.add_field(name="TASK", value=tasks, inline=True)

    return embed

