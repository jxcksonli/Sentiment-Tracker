import asyncio

from backend.app.todo import fetch_hn_comment_texts

async def main():
    comments = await fetch_hn_comment_texts("Tesla")
    for c in comments[:3]:
        print(c)
        print("---")

asyncio.run(main())

