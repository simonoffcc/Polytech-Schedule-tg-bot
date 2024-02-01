from aiogram import Router

register_router = Router(name='register')

# todo: разбить пакет src.bot.logic.register на большее кол-во роутеров,
#  т.к. select.py слишком перегружен и нечитаем
