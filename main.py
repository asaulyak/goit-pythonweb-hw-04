import argparse
import asyncio
from logger import logging
from aiopath import AsyncPath
from aioshutil import copyfile


async def read_folder(path: AsyncPath):
    return path.iterdir()


async def copy_file(source: AsyncPath, destination: AsyncPath):
    await copyfile(source, destination)
    logging.info(f"Copied from {source} to {destination}")


async def copy_content(source: AsyncPath, destination: AsyncPath):
    try:
        async for item in await read_folder(source):
            path = AsyncPath(item)
            current_path = AsyncPath(".") / path

            is_file = await current_path.is_file()
            if is_file:
                suffix = path.suffix
                extension = suffix if suffix else "(no extension)"

                destination_folder_path = destination / AsyncPath(extension).name
                destination_file_path = destination_folder_path / path.name

                await destination_folder_path.mkdir(parents=True, exist_ok=True)
                await copy_file(current_path, destination_file_path)
            else:
                await copy_content(current_path, destination)

    except Exception as e:
        logging.info(f"Failed to copy files from {source} to {destination}: {e}")


async def main():
    logging.info("Start app")
    parser = argparse.ArgumentParser(
        prog="File Mapper",
        description="Copies files to the folders based on the extension",
    )

    parser.add_argument("source")
    parser.add_argument("output")

    args = parser.parse_args()

    await copy_content(AsyncPath(args.source), AsyncPath(args.output))


if __name__ == "__main__":
    asyncio.run(main())
