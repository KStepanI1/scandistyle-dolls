import os

import django
from aiogram.utils import executor

from loader import dp
from utils import set_default_commands
from utils.on_startup_notify import on_startup_notify


async def on_startup(dispatcher):
    import middlewares
    import filters
    import handlers
    middlewares.setup(dp)
    filters.setup(dp)

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)



def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.scandistyle_dolls.settings"
    )
    os.environ.update(
        {"DJANGO_ALLOW_ASYNC_UNSAFE": " true"}
    )
    django.setup()


if __name__ == "__main__":
    setup_django()
    executor.start_polling(dp, on_startup=on_startup)
