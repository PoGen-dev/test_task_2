
import asyncio
import httpx
import logging

from main import app 

async def test_concurrent_requests():
    """
    Make n requests (n=5). Check:

    1) status_code == 200
    2) current elapsed - previous elapsed >= 3
    """
    try: 
        async with httpx.AsyncClient(app=app, base_url="http://0.0.0.0") as client:
            #   Make requests
            tasks = [asyncio.create_task(client.get("/test")) for i in range(5)]
            responses = await asyncio.gather(*tasks)

            #   Perform checks
            prev_elapsed = None
            for response in responses:
                assert response.status_code == 200
                elapsed = response.json()['elapsed']
                if prev_elapsed is not None:
                    assert elapsed - prev_elapsed >= 3.0
                prev_elapsed = elapsed
    except Exception as e: 
        logging.exception(e)

if __name__ == "__main__":
    asyncio.run(test_concurrent_requests())
