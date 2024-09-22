"""
This is a simple FastAPI application that generates random data points and returns them as a list.
"""

import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_data")
async def get_data():
    """
    This endpoint generates a list of random data points.
    """
    data = []
    for _ in range(0, 10):
        random_x = random.randint(0, 100)
        random_y = random.randint(0, 100)
        data.append((random_x, random_y))
    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
