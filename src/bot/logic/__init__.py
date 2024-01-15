from .register import register_router
from .start import start_router
from .get_schedule import get_schedule_router
from .info import info_router
from .unknown_msg import unknown_message

routers = (start_router, register_router, get_schedule_router, info_router, unknown_message,)
