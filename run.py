import sys
import os

import fastapi
import uvicorn
# from core.data_manager import DataManager
from core.data_manager import data_manager

app = fastapi.FastAPI()


# Add the parent directory of 'api' and 'core' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

        
# project_root = os.path.dirname(current_dir)  
# sys.path.insert(0, project_root)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Data Manager API"}
@app.get("/data/{item_id}")
async def read_data(item_id: int):
    item = await data_manager.get_item(item_id)
    if item:
        return item
    return {"error": "Item not found"}

@app.post("/data/")
async def create_data(item: dict):
    item_id = await data_manager.add_item(item)
    return {"item_id": item_id}

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)


