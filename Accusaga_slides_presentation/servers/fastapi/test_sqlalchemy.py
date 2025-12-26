from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

async def test():
    # URL that worked
    url = "sqlite+aiosqlite:///./test.db"
    connect_args = {"check_same_thread": False}
    
    print(f"Testing {url} with {connect_args}")
    try:
        engine = create_async_engine(url, connect_args=connect_args)
        async with engine.connect() as conn:
            print(f"Success: {url}")
    except Exception as e:
        print(f"Failed {url}: {e}")

if __name__ == "__main__":
    asyncio.run(test())
