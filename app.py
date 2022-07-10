import hashlib

from aiogram import Bot, Dispatcher, types, executor
import config
import markups
from db_controller import SQLiteDataBase

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)
db = SQLiteDataBase('preview_bot.db')


@dp.message_handler(commands=['start', 'help'])
async def commands(message: types.Message):
    if message.text == '/start':
        await message.answer(
            f"Hi, {message.chat.username}. Send me the youtube video link and I'll send you a preview.",
            reply_markup=markups.creator_markup())
        db.add_user(message.chat.id)
    elif message.text == '/help':
        await message.answer('Do you have a question? Write to @ondrujko')


@dp.message_handler(content_types=['text'])
async def msg(message: types.Message):
    if 'youtu' in message.text:
        try:
            video_id = message.text.replace('http://', '') \
                .replace('https://', '') \
                .replace('youtu.be', '') \
                .replace('/', '') \
                .replace('www.', '') \
                .replace('youtube.com', '') \
                .replace('watch?v=', '') \
                .split('?')[0]

            await message.answer_media_group(
                [types.InputMediaDocument(f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'),
                 types.InputMediaDocument(f'https://i.ytimg.com/vi/{video_id}/sddefault.jpg'),
                 types.InputMediaDocument(f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'),
                 types.InputMediaDocument(f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'),
                 types.InputMediaDocument(f'https://i.ytimg.com/vi/{video_id}/default.jpg')])
            db.add_action(message.chat.id, video_id)

        except:
            await message.reply('Incorrect link!')
    elif message.text == 'Order development🦾':
        await message.answer('You can order the development from 👉@ondrujko', reply_markup=markups.creator_markup())
    else:
        await message.answer("Send me the youtube video link and I'll send you a preview.",
                             reply_markup=markups.creator_markup())


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    video_id = query.query.replace('http://', '') \
        .replace('https://', '') \
        .replace('youtu.be', '') \
        .replace('/', '') \
        .replace('www.', '') \
        .replace('youtube.com', '') \
        .replace('watch?v=', '') \
        .split('?')[0]
    ph = [types.InlineQueryResultPhoto(id=hashlib.md5(f'{text}'.encode()).hexdigest(),
                                       photo_url=f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg',
                                       thumb_url=f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg')]
    await query.answer(ph, cache_time=60, is_personal=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
