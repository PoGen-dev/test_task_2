from fastapi import FastAPI
from pydantic import BaseModel
from time import monotonic

import asyncio
import uvicorn

app = FastAPI()

# Semaphore with one available slot to ensure concurrent execution of 
# only one func work()
work_semaphore = asyncio.Semaphore(1)

class TestResponse(BaseModel):
    elapsed: float

async def work() -> None:
    await asyncio.sleep(3)

@app.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic()
    
    # Get access to Semaphore
    async with work_semaphore:
        # call func work
        await work()
    
    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)