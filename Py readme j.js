async function fetchDocumentation() {
    // 1. Get the module names the user typed into the web page
    const v1 = document.getElementById("module1-input").value;
    const v2 = document.getElementById("module2-input").value;
    
    // 2. Package the request as JSON and send it to the local Python server (port 8000)
    const response = await fetch("http://localhost:8000/generate-docs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "module_v1": v1,
            "module_v2": v2
        })
    });
    
    // 3. Receive the JSON response from Python and display the AI text on the website
    const data = await response.json();
    document.getElementById("doc-display").innerText = data.documentation;
}

