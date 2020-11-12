"""
From https://docs.python.org/3/library/asyncio-task.html#creating-tasks 
and https://stackoverflow.com/questions/54787401/how-to-properly-use-asyncio-first-completed
for help exit out of async tasks when uvicorn reloads
"""
import asyncio

from uvicorn.main import Server

original_handler = Server.handle_exit


class AppStatus:
    should_exit = False
    exit_event = asyncio.Event()

    @staticmethod
    def handle_exit(*args, **kwargs):
        AppStatus.should_exit = True
        AppStatus.exit_event.set()
        original_handler(*args, **kwargs)


Server.handle_exit = AppStatus.handle_exit


async def wait_until_exit(task):
    tasks = [AppStatus.exit_event.wait(), task]
    _, unfinished = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in unfinished:
        task.cancel()
