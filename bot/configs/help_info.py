from . import config


SUMMARY = 'QmpEla pomaga utrzymać Ciebie i Twoich przyjaciół na dobrej drodze podczas wspólnej nauki!\n' \
          'Wyznacz okresy skupienia na wykonanie pracy i rozmawiaj podczas przerw.\n\n' \
          'Wymagane parametry są ujęte w <>, a opcjonalne w [].\n' \
          f'Na przykład, możesz zrobić \"{config.CMD_PREFIX}start\" aby rozpocząć sesję pomodoro z wartościami domyślnymi ' \
          f'lub \"{config.CMD_PREFIX}start 30 10\" aby dostosować czas trwania pomodoro i krótkich przerw!\n'

POMO_ARGS = 'pomodoro: czas trwania każdego interwału pomodoro w minutach (Domyślnie: 20 min)\n' \
            'short_break: czas trwania krótkich przerw w minutach (Domyślnie: 5 min)\n' \
            'long_break: czas trwania długich przerw w minutach (Domyślnie: 15 min)\n' \
            'intervals: liczba odstępów pomodoro pomiędzy każdą długą przerwą (Domyślnie: 4)'

COUNTDOWN_ARGS = 'Enclose title in " " if longer than one word (Default: \"Countdown\").\n' \
                 'Add the \"mute\" parameter to disable the voice channel audio alert.\n\n' \
                 f'Example usage: {config.CMD_PREFIX}countdown 5 \"Finish homework!\" mute'

COMMANDS = {'Control commands': {'start': ['start [pomodoro] [short_break] [long_break] [intervals]',
                                           'Rozpocznij sesję pomodoro z opcjonalnymi ustawieniami własnymi.\n\n' + POMO_ARGS],
                                 'pause': ['pause', 'Pause session'],
                                 'resume': ['resume', 'Resume session'],
                                 'restart': ['restart', 'Restart timer'],
                                 'skip': ['skip', 'Pomiń bieżący interwał i rozpocznij następne pomodoro lub przerwę.'],
                                 'stop': ['stop', 'End session'],
                                 'edit': ['edit <pomodoro> [short_break] [long_break] [intervals]',
                                          'Kontynuuj sesję z nowymi ustawieniami\n\n' + POMO_ARGS],
                                 'countdown': ['countdown <duration> [title] [mute]',
                                               'Rozpocznij odliczanie, które wysyła przypiętą wiadomość '
                                               'z zegarem, który aktualizuje się w czasie rzeczywistym.\n\n' +
                                               COUNTDOWN_ARGS]
                                 },
            'Info commands': {'time': ['time', 'Get time remaining'],
                              'stats': ['stats', 'Get session stats'],
                              'settings': ['settings', 'Get session settings'],
                              'servers': ['servers', 'See how many servers are using Pomomo']},
            'Subscription commands': {'dm': ['dm', 'Toggle subscription to get DM alerts for the server\'s session.'],
                                      'autoshush': ['autoshush [all]', 'Toggle subscription to get automatically'
                                                                       ' deafened and muted during '
                                                                       'pomodoro intervals.\n'
                                                                       'Members with mute and deafen permissions '
                                                                       'can add the \"all\" parameter to auto_shush '
                                                                       'everyone in the pomodoro voice channel.']}}

LINKS = 'Milej nauki' \
        ';*'
