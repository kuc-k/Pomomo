import time as t

from discord.ext import commands

from src.Settings import Settings
from configs import config, bot_enum, user_messages as u_msg
from src.session import session_manager, session_controller, session_messenger, countdown, state_handler
from src.session.Session import Session
from src.utils import msg_builder


class Control(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx, pomodoro=20, short_break=5, long_break=15, intervals=4):
        if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
            return
        if session_manager.active_sessions.get(session_manager.session_id_from(ctx.channel)):
            await ctx.send(u_msg.ACTIVE_SESSION_EXISTS_ERR)
            return
        if not ctx.author.voice:
            await ctx.send('Dołącz do kanału głosowego, aby korzystać z Pomi!')
            return

        session = Session(bot_enum.State.POMODORO,
                          Settings(pomodoro, short_break, long_break, intervals),
                          ctx)
        await session_controller.start(session)

    @start.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)

    @commands.command()
    async def stop(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            if session.stats.pomos_completed > 0:
                await ctx.send(f'Świetna robota! '
                               f'Ukończyłeś {msg_builder.stats_msg(session.stats)}.')
            else:
                await ctx.send(f'Do zobaczenia wkrótce! 👋')
            await session_controller.end(session)

    @commands.command()
    async def pause(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            timer = session.timer
            if not timer.running:
                await ctx.send('Timer jest już wstrzymany.')
                return

            await session.auto_shush.unshush(ctx)
            timer.running = False
            timer.remaining = timer.end - t.time()
            await ctx.send(f'Wstrzymywanie {session.state}.')
            session.timeout = t.time() + config.PAUSE_TIMEOUT_SECONDS

    @commands.command()
    async def resume(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            timer = session.timer
            if session.timer.running:
                await ctx.send('Timer jest już uruchomiony.')
                return

            timer.running = True
            timer.end = t.time() + timer.remaining
            await ctx.send(f'Wznawianie {session.state}.')
            await session_controller.resume(session)

    @commands.command()
    async def restart(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            session.timer.set_time_remaining()
            await ctx.send(f'Restartowanie {session.state}.')
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.start(session)
            else:
                await session_controller.resume(session)

    @commands.command()
    async def skip(self, ctx):
        session = await session_manager.get_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Odliczeń nie można pomijać. '
                     f'Użyj {config.CMD_PREFIX}stop, aby zakończyć lub {config.CMD_PREFIX}restart, aby zacząć od nowa.')
        if session:
            stats = session.stats
            if stats.pomos_completed >= 0 and \
                    session.state == bot_enum.State.POMODORO:
                stats.pomos_completed -= 1
                stats.minutes_completed -= session.settings.duration

            await ctx.send(f'Pomijanie {session.state}.')
            await state_handler.transition(session)
            await session_controller.resume(session)

    @commands.command()
    async def edit(self, ctx, pomodoro: int, short_break: int = None, long_break: int = None, intervals: int = None):
        session = await session_manager.get_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Odliczeń nie można edytować. '
                     f'Użyj {config.CMD_PREFIX}odliczanie do rozpoczęcia nowego.')
        if session:
            if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
                return
            await session_controller.edit(session, Settings(pomodoro, short_break, long_break, intervals))
            session.timer.set_time_remaining()
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.update_msg(session)
            await session_controller.resume(session)

    @edit.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)

    @commands.command()
    async def countdown(self, ctx, duration: int, title='Odliczanie', audio_alert=None):
        session = session_manager.active_sessions.get(session_manager.session_id_from(ctx.channel))
        if session:
            await ctx.send('Trwa aktywna sesja. '
                           'Czy na pewno chcesz rozpocząć odliczanie? (y/n)')
            response = await self.client.wait_for('message', timeout=60)
            if not response.content.lower()[0] == 'y':
                await ctx.send('OK, anuluję nowe odliczanie.')
                return

        if not 0 < duration <= 180:
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        session = Session(bot_enum.State.COUNTDOWN,
                          Settings(duration),
                          ctx)
        await countdown.handle_connection(session, audio_alert)
        session_manager.activate(session)
        await session_messenger.send_countdown_msg(session, title)
        await countdown.start(session)

    @countdown.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)


def setup(client):
    client.add_cog(Control(client))
