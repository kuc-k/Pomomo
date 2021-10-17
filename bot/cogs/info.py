from random import choice

from discord.ext import commands

from src.session import session_manager
from src.utils import msg_builder
from configs import user_messages as u_msg, bot_enum


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=''):
        help_embed = msg_builder.help_embed(command)
        if help_embed:
            await ctx.send(embed=help_embed)
        else:
            await ctx.send('Wprowadź prawidłową komendę.')

    @commands.command()
    async def time(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            await ctx.send(f'{session.timer.time_remaining_to_str()} pozostały na {session.state}!')

    @commands.command()
    async def settings(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            if session.state == bot_enum.State.COUNTDOWN:
                await ctx.send('Odliczania nie mają ustawień.')
            else:
                await ctx.send(embed=msg_builder.settings_embed(session))

    @commands.command()
    async def stats(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            if session.state == bot_enum.State.COUNTDOWN:
                await ctx.send('Odliczania nie mają statystyk.')
            else:
                stats = session.stats
                if stats.pomos_completed > 0:
                    await ctx.send(f'Ukończyłeś {msg_builder.stats_msg(stats)} do tej pory. ' +
                                   choice(u_msg.ENCOURAGEMENTS))
                else:
                    await ctx.send('Nie ukończyłeś jeszcze żadnej sesji pomodoro.')

    @commands.command()
    async def servers(self, ctx):
        await ctx.send(f'Pomi jest na {len(self.client.guilds)} serwerach '
                       f'z {len(session_manager.active_sessions)} aktywnych sesji!')


def setup(client):
    client.add_cog(Info(client))
