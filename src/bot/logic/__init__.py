from .register import register_router
from .start import start_router
from .get_schedule import get_schedule_router
from .info import info_router
from .unknown_msg import unknown_message

routers = (register_router, start_router, get_schedule_router, info_router, unknown_message,)
