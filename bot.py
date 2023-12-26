from scrape import config,scrapeSubmissions_async
import discord
from discord.ext import tasks,commands
import psycopg2
import random
import re


conn = psycopg2.connect(
    dbname=config['dbname'],
    user=config['user'],
    password=config['password'],
    host=config['host'],
    port=config['port']
)

cursor = conn.cursor()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

def isValidGymLink(link):
    pattern = r"(https?://)?(www\.)?codeforces.com/(contest|gym)/\d+$"
    if re.match(pattern, link):
        return True
    else:
        return False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    adam.start()

@bot.command()
@commands.has_permissions(administrator=True)
async def addwatch(ctx, *args): # args[0] is the name of the watch, args[1] is the mashup link, args[2] is the notification channel
   if len(args) < 3 :
       await ctx.reply("Wrong format! The correct usage of the addwatch command is `!addwatch <name> <mashup link> <channel id>`!")
       return
   if isValidGymLink(args[1]) == False:
       await ctx.reply("Please provide a valid mashup link!")
       return
   cursor.execute("SELECT COUNT(*) FROM watches WHERE (name = %s OR gymlink = %s) AND serverid = %s", (args[0], args[1], str(ctx.guild.id)))
   result = cursor.fetchone()
   if result[0] > 0:
    await ctx.reply("There is already a watch in this server that contains either the provided name or the provided mashup link!")
   else:
    cursor.execute("INSERT INTO watches (name, serverid, gymlink, channelid) VALUES (%s, %s, %s, %s)", (args[0], str(ctx.guild.id), args[1], args[2]))
    conn.commit()
    await ctx.reply("Watch " + args[0] + " added successfully!")

@addwatch.error
async def addwatch_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have the necessary permissions to use this command.")

@bot.command()
@commands.has_permissions(administrator=True)
async def remwatch(ctx, *args): # args[0] is the name of the watch, args[1] is the mashup link
   if len(args) < 1 :
       await ctx.reply("Wrong format! The correct usage of the remwatch command is `!remwatch <name>`!")
       return
   cursor.execute("SELECT id FROM watches WHERE name = %s AND serverid = %s", (args[0], str(ctx.guild.id)))
   print(args[0])
   result = cursor.fetchone()
   if result:
    print(result[0])
    cursor.execute("DELETE FROM watches WHERE name=%s AND serverid=%s", (args[0], str(ctx.guild.id)))
    cursor.execute("DELETE FROM processed WHERE watchid=%s", (str(result[0]),))
    conn.commit()
    await ctx.reply("Watch " + args[0] + " removed successfully!")
   else:
    await ctx.reply("There is no such watch for this server!")

@remwatch.error
async def remwatch_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have the necessary permissions to use this command.")


@bot.command()
async def watches(ctx):
    cursor.execute("SELECT * FROM watches WHERE serverid = %s", (str(ctx.guild.id),))
    result = cursor.fetchall()

    color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    embed = discord.Embed(title=f"Watches for {ctx.guild.name}", color=color)
    
    for watch in result:
        link_text = f"Mashup: [here]({watch[4]})\n<#{watch[3]}>"
        embed.add_field(name=watch[2], value=link_text, inline=False)


    await ctx.send(embed=embed)


async def sendMessage(submission, watch):
   color = discord.Color.from_rgb(255, 0, 0)
   if submission['verdict'] == "Accepted" or submission['verdict'] == "Perfect result: 100 points":
       color = discord.Color.from_rgb(0, 255, 0)
   id_link = f"[{submission['id']}]({watch[4]}/submission/{submission['id']})"
   embed = discord.Embed(title=f"Submission: {watch[2]}", color=color)
   author_link = f"[{submission['author']}](https://codeforces.com/profile/{submission['author']})"
   embed.add_field(name="id", value=id_link, inline=True)
   embed.add_field(name="Problem", value=submission['problem'], inline=True)
   embed.add_field(name="Verdict", value=submission['verdict'] + "\n", inline=True)
   embed.add_field(name="Time", value=submission['time'], inline=True)
   embed.add_field(name="Memory", value=submission['memory'] + "\n", inline=True)
   embed.add_field(name="Author", value=author_link, inline=True)
   embed.add_field(name="Language", value=submission['lang'], inline=True)
   channel = bot.get_channel(int(watch[3]))
   if channel:
      await channel.send(embed=embed)

@tasks.loop(seconds=300)
async def adam():
   cursor.execute("SELECT * FROM watches")
   result = cursor.fetchall()
   for watch in result:
      submissions = await scrapeSubmissions_async(watch[4] + "/status")
      submissions.reverse()
      for submission in submissions:
         cursor.execute("SELECT COUNT(*) FROM processed WHERE submissionid=%s AND watchid=%s", (submission['id'], str(watch[0])))
         results2 = cursor.fetchall()
         if(results2[0][0] == 0):
            cursor.execute("INSERT INTO processed (submissionid, watchid) VALUES(%s,%s)", (submission['id'], str(watch[0])))
            conn.commit()
            await sendMessage(submission, watch)


bot.run(config['token'])
