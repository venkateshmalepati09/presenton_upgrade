import asyncio
import aiosqlite

async def main():
    try:
        async with aiosqlite.connect("test.db") as db:
            print("Connected async")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
