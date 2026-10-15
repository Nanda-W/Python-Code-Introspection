# AI Python Code Documenter

A full-stack local web application that dynamically analyzes Python scripts and uses a local Large Language Model (Ollama) to automatically generate technical documentation. 

This project was built to demonstrate full-pipeline AI integration, including secure file handling, abstract syntax introspection, and background task management.

## How It Works
1. **Frontend:** A vanilla HTML/JS interface packages uploaded `.py` files using `FormData` and sends them to the backend via a secure `fetch` request.
2. **Backend Processing:** A FastAPI server intercepts the file, temporarily saves it, and dynamically imports it using Python's `importlib`.
3. **Introspection:** The backend uses native `dir()` introspection to extract a complete architectural blueprint of the uploaded script, filtering out built-in methods to isolate custom logic.
4. **AI Generation:** The structural data is injected into a strict prompt and sent to a local Llama 3.2 model via the `ollama` Python library.
5. **Delivery & Cleanup:** The server writes the AI's generated Markdown to a physical file, streams it back to the user's browser as an automatic download, and utilizes FastAPI `BackgroundTasks` to instantly delete the temporary files from the server.

## Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Integration:** Ollama (Llama 3.2), Prompt Engineering
* **Frontend:** HTML, JavaScript, CSS
* **Security:** CORSMiddleware
