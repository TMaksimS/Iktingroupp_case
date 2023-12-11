"""head file for start telegram application"""

import asyncio

from src.telebot import main


if __name__ == "__main__":
    asyncio.run(main())
