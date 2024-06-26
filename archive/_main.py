from twitchio.ext import commands
from archive.vars import *
from archive.mfs import *


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN,
                         prefix='!', initial_channels=WANTED_CHANNELS)
        self.lock = asyncio.Lock()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        async with self.lock:
            letters = [f"@{BOT_NICK}"]
            output_text = ""
            print(
                f'Message from {message.author.name}: {message.content}. Channel: {message.channel.name}')

            if check_for_letters(message.content.lower(), letters) and message.author.name != BOT_NICK and message.author.name not in BLOCKED_USERS:
                if message.channel.name == "k3ned1" and message.author.name == "k3ned1":
                    output_text = generate_ai_message(message.content)
                else:
                    output_text = generate_ai_message(message.content)

                if LOGGING:
                    write_to_log(message.content,
                                 message.author.name, message.channel)
                    write_to_log(output_text, "BOT", message.channel)

                split_text = split_long_gpt(output_text)
                for substr in split_text:
                    await message.channel.send(f"{substr} @{message.author.name}")
                    await asyncio.sleep(DELAY)


bot = Bot()
bot.run()
