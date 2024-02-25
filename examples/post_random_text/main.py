import asyncio
import random

from mipac.client import Client

with open("text.csv", mode="r", encoding="utf-8") as f:
    texts = f.read().rstrip().split("\n")


async def main():
    async with Client("https://misskey.io", "your token here") as client:
        api = client.api

        await api.note.action.create(text=random.choice(texts))


if __name__ == "__main__":
    asyncio.run(main())
