import discord
from discord.ext import tasks, commands

BOT_TOKEN = "BOT_TOKEN"  # Replace with your bot token

# Format: {channel_id: [thread_id1, thread_id2, ...]}
CHANNELS_AND_THREADS = {
    0000000000000000000: [0000000000000000000, 0000000000000000000],
    0000000000000000000: [0000000000000000000, 0000000000000000000],
}

# Replace with the message you want to send
MESSAGE_CONTENT = "Super cool auto message"

intents = discord.Intents.default()
intents.messages = True  
intents.guilds = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!@?#", intents=intents)
# Bot status
@bot.event
async def on_ready():
        await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Messager")
    )
    print(f"Bot logged in as {bot.user}")
    send_and_delete_message.start()  

@tasks.loop(hours=24)  # seconds=10, hours=24, etc. frequency of time
async def send_and_delete_message():
    for channel_id, thread_ids in CHANNELS_AND_THREADS.items():
        channel = bot.get_channel(channel_id)
        if channel:
            for thread_id in thread_ids:
                try:
                    if isinstance(channel, discord.TextChannel):
                        thread = channel.get_thread(thread_id)
                    elif isinstance(channel, discord.ForumChannel):
                        thread = discord.utils.get(channel.threads, id=thread_id)
                    else:
                        thread = None

                    if thread:
                        sent_message = await thread.send(MESSAGE_CONTENT)
                        # Deletes the message after sending, disable if you want message to say
                        await sent_message.delete()
                        print(f"Message sent and deleted successfully in thread {thread_id}.")
                    else:
                        print(f"Thread {thread_id} not found in channel {channel_id}. Please check the ID.")
                except Exception as e:
                    print(f"An error occurred in thread {thread_id}: {e}")
        else:
            print(f"Channel {channel_id} not found. Please check the ID.")

bot.run(BOT_TOKEN)
