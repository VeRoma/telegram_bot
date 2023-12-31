import openai
import json
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

file = open('config.json', 'r')
config = json.load(file)

openai.api_key = config['openai']
# bot = Bot(config['token'])
# dp = Dispatcher(bot)

# Bot token can be obtained via https://t.me/BotFather
TOKEN = config['token']

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

def chatWithGPT(prompt):
  completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
  model="gpt-4-0314",
  messages=[
  {"role": "user", "content": prompt}
  ]
  )
  return completion.choices[0].message.content

def imageWithGPT(queryPrompt):
    response = openai.Image.create(
        prompt = queryPrompt,
        n=1,
        size="1024x1024"
        )
    return response['data'][0]['url']




@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        
        # answer = 
        # await message.answer(chatWithGPT(message.text))

        
       
        await message.answer_photo(imageWithGPT(message.text))

        # message.
        # chatWithGPT(message.text)
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")