import requests
import json

def google_search(query):
    """Fetch search results from Google using SerpAPI."""
    API_KEY = "e6bc0a43ed93d96f8923dde551b861a2176d8b8953c436406305dc32c878027b"  # Replace with your SerpAPI key
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": API_KEY,
        "num": 5  # Limit results to 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        return "\n".join([f"{i+1}. {res['title']}: {res['link']}" for i, res in enumerate(results)])
    return "No results found."

def query_llama(prompt):
    """Send prompt to Ollama's LLaMA 3.2:1B model and return response."""
    url = "http://localhost:11434/api/generate"  # Ollama's local API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}  # Disable streaming

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        # print(data.get("response", "").strip())
        return data.get("response", "").strip()
        # return response.json().get("response", "").strip()
    return "Error in AI processing."

def ai_response(query):
    """Fetch search results and generate AI response."""
    search_results = google_search(query)
    prompt = f"Here are some Google search results:\n{search_results}\n\nGenerate a response based on this information."
    return query_llama(prompt)

if __name__ == "__main__":
    user_query = input("Ask something: ")
    print("\nAI Response:")
    print(ai_response(user_query))
