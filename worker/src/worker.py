import asyncio
from asyncio import sleep as asleep
import json
from os import getenv
from pyrogram import Client, errors, enums
from pyrogram.raw.functions import messages
from pyrogram.raw import functions, types

import config
from config import log

# load_dotenv()
EXAMPLE_CHANNEL_LINK = getenv("EXAMPLE_CHANNEL_LINK", "durov")
API_ID = int(getenv("TELEGRAM_API_ID"))
API_HASH = getenv("TELEGRAM_API_HASH")
MESSAGES_LIMIT = int(getenv("MESSAGES_DEFAULT_LIMIT"), 20)
COMMENTS_LIMIT = int(getenv("COMMENTS_DEFAULT_LIMIT"), 10)


async def parse_group(api_id: int = API_ID, api_hash: str = API_HASH,
                      channel_link: str = EXAMPLE_CHANNEL_LINK,
                      dry_dump_to_file: bool = False,
                      messages_limit: int = MESSAGES_LIMIT,
                      comments_limit: int = COMMENTS_LIMIT,
                      ):
    """
    Parse a Telegram group and return a JSON object containing the group's information.

    :param api_id: Telegram API ID
    :param api_hash: Telegram API hash
    :param channel_link: Link to the channel to parse
    :param channel_id: ID of the channel to parse
    :param dry_dump_to_file: Whether to dump the parsed group to a file
    :param messages_limit: Number of messages to parse
    :param comments_limit: Number of comments to parse
    :return: dict if dry_dump_to_file is False, else a JSON file containing the group's information in the FS

    If channel_id is not None, channel_link will be ignored.
    """

    async with Client("oxb1b1", api_id, api_hash, session_string=config.telegram_session_token) as app:
        group_report = {
            'handle': channel_link,
            'name': None,
            'id': None,
            'about': None,
            'linked_chats': None,
            'participants_count': None,
            'last_message_id': None,
            'messages': {}
        }
        print(f'session = {app.export_session_string()}')
        channel: types.input_peer_channel.InputPeerChannel = await app.resolve_peer(channel_link)
        # Get channel information
        channel_info: types.messages.chat_full.ChatFull = await app.invoke(functions.channels.GetFullChannel(channel=channel))
        group_report['about'] = channel_info.full_chat.about
        group_report['participants_count'] = channel_info.full_chat.participants_count

        # Get channel name and id
        group_report['id'] = channel_info.full_chat.id
        group_report['name'] = [chat.title for chat in channel_info.chats if chat.id == group_report['id']][0]

        # Get comment group (where people comment on posts)
        group_report['linked_chats'] = [[[chat.id, chat.title]] for chat in channel_info.chats if chat.id != channel_info.full_chat.id]

        # Get last 10 messages and display them, their comments and reactions
        print('\n---\nGetting messages...')
        print(channel_info.chats[0])

        try:
            async for message in app.get_chat_history(channel_info.chats[0].username,
                                                      limit=messages_limit):
                msg_report: dict = {
                    'text': None,
                    'file_unique_id': None,
                    'timestamp': None,
                    'reactions': {},
                    'comments': {}
                }

                # Type hintings
                message: types.Message

                # Parse photos and captions
                if not message.media:
                    msg_report['text'] = message.text
                else:
                    msg_report['text'] = message.caption
                    if message.media is enums.MessageMediaType.PHOTO:
                        msg_report['file_unique_id'] = message.photo.file_unique_id

                # Collect timestamp
                msg_report['timestamp'] = message.date
                if dry_dump_to_file:
                    # Convert timestamp to ISO format
                    msg_report['timestamp'] = msg_report['timestamp'].isoformat()

                # Collect reactions
                reactions = message.reactions
                reactions = reactions.reactions if reactions else None
                msg_report['reactions'] = {reaction.emoji: reaction.count for reaction in reactions} if reactions else {}

                comments = {}  # 'message_id': { 'text': str, 'reactions': { '<EMOJI>': 'count' int } }
                try:
                    async for discussion_message in app.get_discussion_replies(message.chat.id, message.id,
                                                                            limit=comments_limit):
                        comment_report: dict = {
                            'text': None,
                            'timestamp': None,
                            'reactions': {}
                        }
                        if discussion_message.media:
                            comment_report['text'] = discussion_message.caption
                        else:
                            comment_report['text'] = discussion_message.text

                        # Collect timestamp
                        comment_report['timestamp'] = discussion_message.date
                        if dry_dump_to_file:
                            # Convert timestamp to ISO format
                            comment_report['timestamp'] = comment_report['timestamp'].isoformat()

                        # Collect reactions
                        reactions = discussion_message.reactions
                        reactions = reactions.reactions if reactions else None
                        comment_report['reactions'] = {reaction.emoji: reaction.count for reaction in reactions} if reactions else {}
                        if not comment_report['text']:
                            log.debug(f'No text in comment {discussion_message.id}; skipping...')
                            continue
                        comments[discussion_message.id] = comment_report
                        log.debug(f"Added comment {discussion_message.id} to message {message.id}")
                except errors.exceptions.bad_request_400.MsgIdInvalid:
                    pass
                except errors.FloodWait as exc:
                    log.info(f'FloodWait: {exc.value} seconds')
                    await asleep(exc.value)

                # Skip the message if both text and file_unique_id are None
                if not msg_report['text'] and not msg_report['file_unique_id']:
                    continue

                # Add comments to msg_report
                msg_report['comments'] = comments

                # Append message to full_info if either text or file_unique_id is not None
                group_report['messages'][message.id] = msg_report
                log.debug(f"Added message {message.id} to group report")
        except errors.FloodWait as exc:
            log.info(f'FloodWait: {exc.value} seconds')
            await asleep(exc.value)
        log.debug(f"Finished parsing messages for channel {channel_link}!")

        # Save group_report to file if dry_dump_to_file is True
        if dry_dump_to_file:
            log.debug("Dumping group report to file...")
            with open(f'{channel_link}-group_report.json', 'w', encoding='UTF8') as f:
                json.dump(group_report, f, indent=4, ensure_ascii=False)
        else:
            log.debug("Returning group report...")
            return group_report


if __name__ == '__main__':
    asyncio.run(parse_group(dry_dump_to_file=True))
