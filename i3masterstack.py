#!/usr/bin/python3 

from i3ipc.aio import Connection 
import asyncio

from i3ipc.events import Event, IpcBaseEvent, WindowEvent

async def set_split_direction(conn: Connection):
    focused = (await conn.get_tree()).find_focused()
    if focused is None:
        return;

    ws = focused.workspace()
    if ws is None:
        return;

    if len(ws.nodes) == 1 and ws.nodes[0].layout != "splith":
        await conn.command(f"[con_id={ws.nodes[0].id}] split h")
    if len(ws.nodes) > 1 and ws.nodes[1].layout != "splitv":
        await conn.command(f"[con_id={ws.nodes[1].id}] split v")

def on_event(conn: Connection, event: IpcBaseEvent):
    asyncio.get_event_loop().create_task(set_split_direction(conn))

async def main():
    i3 = await Connection().connect()

    i3.on(Event.WINDOW_NEW, on_event)
    i3.on(Event.WINDOW_CLOSE, on_event)

    await i3.main()

if __name__ == "__main__":
    asyncio.run(main())
