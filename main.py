from fastapi import FastAPI, HTTPException
from typing import Optional
import os
import subprocess

app = FastAPI()

@app.post("/run")
async def run_task(task: Optional[str] = None):
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        # Simulate task execution
        result = execute_task(task)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def execute_task(task: str):
    if task.startswith("install uv and run datagen.py"):
        email = task.split(" ")[-1]
        try:
            # Install uv package if required
            subprocess.run(["pip", "install", "uv"], check=True)
            # Download datagen.py script
            subprocess.run(["curl", "-O", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"], check=True)
            # Ensure the script is in the current directory
            if not os.path.exists("datagen.py"):
                raise ValueError("datagen.py script not found")
            # Run datagen.py script with the provided email
            result = subprocess.run(["python", "datagen.py", email], check=True, capture_output=True, text=True)
            return {"result": f"Data generation script executed successfully: {result.stdout}"}
        except subprocess.CalledProcessError as e:
            return {"error": f"Error executing task: {e.stderr}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    else:
        return {"error": "Invalid task"}

@app.get("/read")
async def read_file(path: Optional[str] = None):
    if not path:
        raise HTTPException(status_code=400, detail="File path is required")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(path, 'r') as file:
        content = file.read()
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)