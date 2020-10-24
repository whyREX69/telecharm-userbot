from pyrogram import Client, filters
from pyrogram.types import Message

from app import __version__, config
from app.storage import json_settings
from app.utils import clean_up, get_args


@Client.on_message(filters.me & filters.command(['start', 'help', 'share'], prefixes='.'))
async def help_command(client: Client, message: Message):
    """
    Builtin help command to access command list and GitHub repo or share this userbot.
    """
    args = get_args(message.text or message.caption)
    if 'ru' in args:  # Russian version requested
        text = f'**Telecharm v{__version__}**:\n\n`.help` - Английская версия.\n\n' \
               f'__[Список команд]({config.GUIDE_LINK_RU})\n[Telecharm на GitHub]({config.GITHUB_LINK})__'
    else:  # English version requested
        text = f'**Telecharm v{__version__}**:\n\n`.help ru` for Russian\n\n' \
               f'__[List of commands]({config.GUIDE_LINK_EN})\n[Telecharm on GitHub]({config.GITHUB_LINK})__'

    await message.edit_text(text, disable_web_page_preview=True)
    await clean_up(client, message.chat.id, message.message_id, clear_after=15)


@Client.on_message(filters.me & filters.command('cleanup', prefixes='.'))
async def clean_up_switcher(client: Client, message: Message):
    """
    Turn on/off cleaning up mode that deletes messages some time after editing them.
    """
    last_value = json_settings.data.get('clean_up', False)
    json_settings.set('clean_up', not last_value)

    status = 'off' if last_value else 'on'
    await message.edit_text(f'Clean up is **{status}**.')
    await clean_up(client, message.chat.id, message.message_id)
