import json
import os
import psutil
import objgraph
import time

from shutil import copyfile
from discord import Intents
from discord.ext import tasks
from discord.ext.commands import AutoShardedBot

with open("config.json") as f:
    config = json.load(f)


class MemoryChecker(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("[+] Logging in with AutoShardedBot...")
        self.prefix = "SOMEDUMBPREFIXNOBODYGUESSESKTHXBYE"
        self.process = psutil.Process(os.getpid())
        self.last_memory = None

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        self.log_memory_usage.start()

    @tasks.loop(seconds=1)
    async def log_memory_usage(self):
        memory = self.process.memory_info().rss / 1024 ** 2
        memory_rounded = round(memory, 2)

        if memory_rounded == self.last_memory:
            return

        memory_pretty = f"{memory:.2f} MB"
        timestamp = time.time()

        with open("./memory.json", "r") as f:
            data = json.load(f)

        new_append_data = {
            "timestamp": timestamp, "memory": memory, "memory_pretty": memory_pretty
        }

        with open("./memory.json", "w") as f:
            data.append(new_append_data)
            json.dump(data, f)

        with open("./dump.log", "w") as f:
            objgraph.show_growth(file=f, shortnames=False)

        copyfile("./dump.log", f"./dumps/dump_{int(timestamp)}.log")

        print(f"[+] New memory change detected: {memory_pretty} | {timestamp}")
        self.last_memory = memory_rounded


client = MemoryChecker(
    command_prefix="SOMEDUMBPREFIXNOBODYGUESSESKTHXBYE",
    intents=Intents(
        guilds=True, members=True, messages=True, bans=True,
        emojis=True, voice_states=True, presences=True, reactions=True
    )
)

client.run(config["token"])
