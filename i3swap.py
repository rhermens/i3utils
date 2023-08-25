#!/usr/bin/python3

import argparse
from i3ipc.aio import Connection
from dataclasses import dataclass
from i3ipc.replies import WorkspaceReply
import asyncio


@dataclass
class CurrentState():
    primary: WorkspaceReply
    secondary: WorkspaceReply


async def main():
    parser = argparse.ArgumentParser(
        prog="i3swap",
        description="Swap workspaces between monitors"
    )
    i3 = await Connection().connect()

    workspaces = await i3.get_workspaces()
    outputs = list(set([ws.ipc_data.get('output') for ws in workspaces]))

    parser.add_argument(
        "-p",
        "--primary",
        help="Primary monitor",
        default=outputs[0]
    )
    parser.add_argument(
        "-s",
        "--secondary",
        help="Secondary monitor",
        default=outputs[1]
    )

    args = parser.parse_args()
    state = CurrentState(
        primary=next(
            ws for ws in workspaces
            if ws.ipc_data.get("visible")
            and ws.ipc_data.get('output') == args.primary
        ),
        secondary=next(
            ws for ws in workspaces
            if ws.ipc_data.get("visible")
            and ws.ipc_data.get('output') == args.secondary
        ),
    )

    await asyncio.gather(
        i3.command(f"[workspace={state.primary.ipc_data.get('num')}] move workspace to output {state.secondary.ipc_data.get('output')}"),
        i3.command(f"[workspace={state.secondary.ipc_data.get('num')}] move workspace to output {state.primary.ipc_data.get('output')}"),
        i3.command(f"[workspace={state.secondary.ipc_data.get('num')}] focus")
    )


if __name__ == "__main__":
    asyncio.run(main())
