from aiogram import Router

register_router = Router(name='register')
register_router.message.middleware()
