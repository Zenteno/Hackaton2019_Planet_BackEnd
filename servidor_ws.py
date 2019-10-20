#!/usr/bin/env python

import asyncio
import json
import logging
import websockets

logging.basicConfig()

USERS = set()

async def notify_users(message):
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    await notify_users("se ha registrado un nuevo usuario")
    await asyncio.wait([websocket.send("Bienvenido")])
    USERS.add(websocket)
            

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users("se ha ido el usuario x")


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        #await websocket.send(state_event())
        async for message in websocket:
            websocket.send(message)
            #data = json.loads(message)
            #print(data)
            #print(websocket)
            '''
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
            '''
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()