# run this file as python authentication.py inside the streamdjango folder
# ensure django, websockets is installed in the venv
#!/usr/bin/env python
# The file needs to be in the django server folder
# sys.path.append("D:\\gitFolders\\django_projects\\streamdjango")

import asyncio
import sys
import os

import django
import websockets

sys.path.append("D:\\gitFolders\\django_projects\\streamdjango")
os.environ['DJANGO_SETTINGS_MODULE'] = "streamdjango.settings"

django.setup()

from sesame.utils import get_user
from websockets.frames import CloseCode


async def handler(websocket):
    sesame = await websocket.recv()
    user = await asyncio.to_thread(get_user, sesame)
    if user is None:
        await websocket.close(CloseCode.INTERNAL_ERROR, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")


async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())