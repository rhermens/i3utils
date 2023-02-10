#!/usr/bin/python3 

from i3ipc.aio import Connection 
from functools import reduce
import argparse
import asyncio

async def main(args):
    i3 = await Connection().connect()
    workspaces = await i3.get_workspaces()
    nums = [ws.ipc_data.get('num') for ws in workspaces]
    nums.sort()

    highestCurrent = reduce(lambda acc, prev: acc + 1 if prev - acc == 1 else acc, nums, 0)
    next = highestCurrent + 1

    if (args['move']):
        await asyncio.gather(
            i3.command(f'move container to workspace number {next}'),
            i3.command(f'[workspace={next}] focus'),
        )
    else:
        await i3.command(f'workspace number {next}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Go to next i3 workspace")
    parser.add_argument('-m', '--move', action='store_true', help="Move focused container to next workspace")
    args = parser.parse_args()
    asyncio.run(main(vars(args)))
