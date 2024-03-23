from fastapi import FastAPI
from cachetools import TTLCache
from datetime import datetime

app = FastAPI()

# Create a TTL (time-to-live) cache with a maximum size of 1000 and a TTL of 60 seconds
cache = TTLCache(maxsize=1000, ttl=60)

# Sample endpoint with response caching
@app.get("/cached_data")
def get_cached_data():
    # Check if the data is already cached
    cached_data = cache.get("cached_data")
    if cached_data:
        # Return cached data if available
        return {"cached_data": cached_data, "cached_at": datetime.now().isoformat()}

   # If not, generate new data, store it in the cache, and return it
    else:
        new_data = {"value":  42}
        cache["cached_data"] = new_data
        return {"newly generated": new_data, "generated at": datetime.now().isoformat(), **new_data}, 2
    

    # Store the new data in the cache
    cache["cached_data"] = new_data

    return {"cached_data": new_data, "cached_at": datetime.now().isoformat()}
