from redbot.core import commands
from redbot.core import Config
import discord
import asyncio


class Minecraft(commands.Cog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = asyncio.Lock()
        self.config = Config.get_conf(self, identifier=141197)
        # default_member = {}
        default_guild = {
            'connections': {}
        }
        # self.config.register_member(**default_member)
        self.config.register_guild(**default_guild)

    @commands.group(aliases=['mc'])
    async def minecraft(self, ctx):
        pass

    @minecraft.group(aliases=['nether', 'hub'])
    async def nether_hub(self, ctx):
        pass

    @minecraft.group()
    async def locations(self, ctx):
        pass

    @nether_hub.command()
    async def list(self, ctx):
        async with self.lock:
            connections = await self.config.guild(ctx.guild).connections()
            embed = discord.Embed(title="NETHER HUB")
        for connection, portals in connections.items():
            embed.add_field(name=connection.title(), inline=True)
            embed.add_field(name=f"{portals[0]['x']} | {portals[0]['z']}", value="Nether", inline=True)
            embed.add_field(name = f"{portals[1]['x']} | {portals[1]['y']} | {portals[1]['y']}", value = "Overworld",
                            inline = True)
        return await ctx.send(embed=embed)

    @nether_hub.command()
    async def add(self, ctx, name: str, nether_x: int, nether_z: int, overworld_x: int, overworld_y: int,
                  overworld_z: int):
        nether_portal = {'x': nether_x, 'z': nether_z}
        overworld_portal = {'x': overworld_x, 'y': overworld_y, 'z': overworld_z}
        async with self.lock:
            data = await self.config.guild(ctx.guild).all()
        if name.lower() in data['connections'].keys():
            return await ctx.send("There is already a connection with that name.")
        else:
            data['connections'][name.lower()] = [nether_portal, overworld_portal]
        await self.config.guild(ctx.guild).connections.set(data['connections'])
        return await ctx.send("The connection has been registered.")

