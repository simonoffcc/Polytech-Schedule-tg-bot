from .help import help_router
from .start import start_router
from .get_schedule import get_schedule_router
from .unknown_msg import unknown_message

routers = (start_router, get_schedule_router, help_router, unknown_message)
