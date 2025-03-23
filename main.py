import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s -%(message)s')

    logger.info('Starting bot') #начало работы бота

    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    #Настраиваем кнопки меню
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере, порядок важен!
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True) #пропускаем накопившие апдейты
    await dp.start_polling(bot)                         #запускаем поллинг

asyncio.run(main())