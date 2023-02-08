#!/usr/bin/python3 

from i3ipc.aio import Connection 
from dataclasses import dataclass
from i3ipc.replies import WorkspaceReply

@dataclass
class CurrentState():
    primary: WorkspaceReply
    secondary: WorkspaceReply

async def main():
    i3 = await Connection().connect()
    workspaces = await i3.get_workspaces()
    filteredWorkspaces = [ws for ws in workspaces if ws.ipc_data.get("visible")]

    workspaces = CurrentState(
        primary=next(ws for ws in filteredWorkspaces if ws.ipc_data.get("focused")),
        secondary=next(ws for ws in filteredWorkspaces if not ws.ipc_data.get("focused"))
    )

    await asyncio.gather(
        i3.command(f"[workspace={workspaces.primary.ipc_data.get('num')}] move workspace to output {workspaces.secondary.ipc_data.get('output')}"),
        i3.command(f"[workspace={workspaces.secondary.ipc_data.get('num')}] move workspace to output {workspaces.primary.ipc_data.get('output')}"),
        i3.command(f"[workspace={workspaces.secondary.ipc_data.get('num')}] focus")
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
