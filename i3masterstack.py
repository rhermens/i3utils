#!/usr/bin/python3 

from i3ipc.aio import Connection 
import asyncio

from i3ipc.events import Event

async def set_split_direction(conn: Connection):
    focused = (await conn.get_tree()).find_focused()
    if focused is None:
        return;

    ws = focused.workspace()
    if ws is None:
        return;

    print(len(ws.nodes))

    if len(ws.nodes) == 1 and ws.nodes[0].layout != "splith":
        print("splitting h")
        await conn.command(f"[con_id={ws.nodes[0].id}] split h")
    if len(ws.nodes) > 1 and ws.nodes[1].layout != "splitv":
        print("splitting v")
        await conn.command(f"[con_id={ws.nodes[1].id}] split v")
    if len(ws.nodes) > 2:
        commands = []
        target = ws.nodes[1].nodes[len(ws.nodes[1].nodes) - 1]
        for node in ws.nodes[2:]:
            commands.append(conn.command(f"[con_id={target.id}] mark {target.id}; [con_id={node.id}] move to mark {target.id}; [con_id={target.id}] unmark;"))
        await asyncio.gather(*commands)

async def main():
    i3 = await Connection().connect()

    i3.on(Event.WINDOW_NEW, lambda conn, _: None if asyncio.get_event_loop().create_task(set_split_direction(conn)) else None)
    i3.on(Event.WINDOW_CLOSE, lambda conn, _: None if asyncio.get_event_loop().create_task(set_split_direction(conn)) else None)
    i3.on(Event.WINDOW_MOVE, lambda conn, _: None if asyncio.get_event_loop().create_task(set_split_direction(conn)) else None)

    await i3.main()

if __name__ == "__main__":
    asyncio.run(main())
