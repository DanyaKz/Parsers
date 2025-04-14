from telethon import TelegramClient, events, types, errors
import logging
import pandas as pd
import json

# Logging configuration
logging.basicConfig(format='l%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

api_id = 0  # Your api_id (SECRET — replace with actual ID)
api_hash = 'api_hash'  # Your api_hash (SECRET — replace with actual hash)

# Keywords to search for in message text
keywords = ['вакцина', 'вакцинация', 'вакцинациясы', 'вакцинациядан', 'тарту',  'иммунизациясы', 'екпе', 
'прививка', 'иммунизация'] 

# Tracked emojis for reactions count
tracked_emoji = ['👍', '❤️', '🔥']

# Telegram channel to parse messages from
channel_username = 'channel_name'


async def main():
    count = 0
    async with TelegramClient('parser', api_id, api_hash) as client:
        comments = [] 

        # Iterate over all messages in the channel
        async for message in client.iter_messages(channel_username):
            if message.text is not None and any(keyword in message.text.lower() for keyword in keywords):
                msgID = message.id
                source = f"https://t.me/{channel_username}/{msgID}"
                try:
                    # Fetch replies to the message
                    async for comment in client.iter_messages(channel_username, reply_to=msgID, reverse=True):
                        if comment.text is not None:
                            sender = comment.sender
                            
                            # Get sender name or use default for deleted accounts
                            sender_name = sender.first_name if isinstance(sender, types.User) else "deleted account"

                            num_reactions = 0
                            # Count reactions with tracked emojis
                            if isinstance(comment.reactions, types.MessageReactions):
                                for r in comment.reactions.results:
                                    if r.reaction.emoticon in tracked_emoji:
                                        num_reactions += r.count

                            # Append the formatted comment to the list
                            comments.append({
                                'Nickname': sender_name,
                                'Date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                                'Likes': num_reactions,
                                'Comment': comment.text,
                                'Source': source
                            })
                            
                except errors.rpcerrorlist.MsgIdInvalidError as msgIdError:
                    logging.error("%s, Source: %s", msgIdError, source)
                except Exception as e:
                    logging.error("%s, Source: %s", e, source)

        # Save results to JSON file
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({'tg': comments}, f, ensure_ascii=False, indent=4)

# Run the main function
import asyncio
asyncio.run(main())
