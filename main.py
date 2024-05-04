import config
import random

from twitchio.ext import commands

# commands = {
#     "!очередь": None,

# }



class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=config.TWITCH_TOKEN, prefix='!', initial_channels=config.CHANNELS)
        self.queue = []
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        author = message.author
        if message.echo:
            return
        commands = {
            "!очередь": (self.list_queue, ()),
            "!войти": (self.join_queue, (author.name,)),
            "!выйти": (self.quit_queue, (author.name,))
        }
        admin_commands = {
            "!kick": self.kick_from_queue,
            "!next": self.call_from_queue,
            "!reset": self.reset_queue,
            "!random": self.random
        }

        content = message.content.split(" ")
        print(f"{content=}")
        command_name = content[0]
        if command_name in commands:
            command, args = commands[command_name]
            await command(*args)
        
        
        if command_name in admin_commands and int(author.id) == self.user_id:
            args = ()
            if len(content) == 2:
                target = content[1]
                args = (target, )
            command = admin_commands[command_name]
            await command(*args)

    

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')
    
    async def list_queue(self):
        queue = ", ".join(self.queue[::-1])
        text = f"Текущая очередь: {queue}" if queue else "В очереди никого нет. Ты можешь стать первым ;) Чтобы записаться, напшии в чат !войти"
        await self.connected_channels[0].send(text)

    async def join_queue(self, target):
        self.queue.insert(0, target)
        await self.list_queue()

    async def quit_queue(self, target):
        self.queue.remove(target)
        await self.list_queue()

    async def kick_from_queue(self, target):
        print(self.queue)
        self.queue.remove(target.lstrip("@").lower())
        await self.list_queue()
    
    async def call_from_queue(self):
        next_player = self.queue[-1]
        self.queue.remove(next_player)
        # next_player = self.queue.copy().reverse().pop(0)
        await self.connected_channels[0].send(f"Следующий по очереди: {next_player}")
        await self.list_queue()
        
    async def reset_queue(self):
        self.queue = []
        await self.list_queue()
    
    async def random(self):
        player = random.choice(self.queue)
        self.queue.remove(player)
        await self.connected_channels[0].send(f"Следующий: {player}")
        await self.list_queue()

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.