# import httpx
# import asyncio
# from typing import List, Optional

# async def fetch_convo(client: httpx.AsyncClient, user_id: str, convo_id: str):
#     url = f"https://mr-mvp-api-dev.dev.ingenspark.com/Db_store_router/conversations/{convo_id}"
#     try:
#         # Pass user_id as a query parameter as shown in the request
#         r = await client.get(url, params={"user_id": user_id}, timeout=30)
#         r.raise_for_status()
        
#         # Parse the response safely
#         json_data = r.json()
#         data = json_data.get("conversation") or (json_data.get("conversations") or [None])[0]
        
#         if not data: 
#             return None
            
#         resp = data.get("response", {})
#         return {
#             "query": data.get("user_query", {}).get("text", ""), 
#             "response": resp.get("text", "")
#         }
#     except Exception as e:
#         print(f"Error fetching {convo_id}: {e}")
#         return None

# async def fetch_all(user_id: str, convo_ids: List[str]):
#     async with httpx.AsyncClient() as client:
#         tasks = [fetch_convo(client, user_id, cid) for cid in convo_ids]
#         results = await asyncio.gather(*tasks)
#         return [r for r in results if r]


import httpx
import asyncio
import logging
from typing import List

logger = logging.getLogger(__name__)

async def fetch_all(user_id: str, convo_ids: List[str]):
    url = "https://mr-mvp-api-dev.dev.ingenspark.com/Db_store_router/conversations/{}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [client.get(url.format(cid), params={"user_id": user_id}) for cid in convo_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        data = []
        for idx, r in enumerate(results):
            if isinstance(r, Exception):
                continue
            try:
                r.raise_for_status()
                json_data = r.json()
                conv = json_data.get("conversation") or (json_data.get("conversations") or [None])[0]
                if conv:
                    query = conv.get("user_query", {}).get("text", "")
                    response = conv.get("response", {}).get("text", "")
                    if query or response:
                        data.append({"query": query, "response": response})
            except Exception as e:
                logger.error(f"Error: {e}")
        return data
