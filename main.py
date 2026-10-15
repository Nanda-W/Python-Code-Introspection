from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import importlib
import ollama
import uvicorn
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# A helper function to clean up files
def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/generate-readme")
async def generate_readme(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 1. Save uploaded file temporarily
    file_location = f"{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Extract structure
    module_name = file.filename.replace(".py", "")
    try:
        mod = importlib.import_module(module_name)
        importlib.reload(mod)
        features = {attr for attr in dir(mod) if not attr.startswith("__")}
    except Exception as e:
        return {"error": f"Could not read python file: {str(e)}"}
        
    # 3. Generate text with Ollama
    prompt = (
        f"You are a technical writer. Create a detailed README.md file for a Python script.\n"
        f"The complete list of functions and variables is: {features}.\n"
        "Explain what a program with these functions likely does, and write a brief description for each one."
    )
    response = ollama.generate(model='llama3.2', prompt=prompt)
    
    # 4. Save the AI's text to a new Markdown file
    output_name = f"{module_name}_README.md"
    with open(output_name, "w") as output_file:
        output_file.write(response['response'])
    
    # 5. Tell the server to delete both files AFTER the download completes
    background_tasks.add_task(remove_file, file_location)
    background_tasks.add_task(remove_file, output_name)
    
    # 6. Send the physical file back to the browser
    return FileResponse(output_name, media_type="text/markdown", filename=output_name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)