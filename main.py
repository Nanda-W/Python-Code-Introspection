from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import importlib
import ollama
import uvicorn
import shutil
import os

app = FastAPI()

# Allow the web page to talk to the local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-readme")
async def generate_readme(file: UploadFile = File(...)):
    # 1. Save the uploaded file temporarily to the server folder
    file_location = f"{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Strip the ".py" from the filename so importlib can read it
    module_name = file.filename.replace(".py", "")
    
    # 3. Extract the structure
    try:
        mod = importlib.import_module(module_name)
        importlib.reload(mod) # Reload ensures we get the newest version if you upload twice
        features = {attr for attr in dir(mod) if not attr.startswith("__")}
    except Exception as e:
        return {"error": f"Could not read python file: {str(e)}"}
        
    # 4. Construct the prompt
    prompt = (
        f"You are a technical writer. Create a detailed README.md file for a Python script.\n"
        f"The complete list of functions and variables in this script is: {features}.\n"
        "Explain what a program with these functions likely does, and write a brief description for each one."
    )
    
    # 5. Ask Ollama to generate the README
    response = ollama.generate(model='llama3.2', prompt=prompt)
    
    # (Optional) Clean up: Delete the file after reading it
    os.remove(file_location)
    
    # 6. Send the text back to the website
    return {"readme": response['response']}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)