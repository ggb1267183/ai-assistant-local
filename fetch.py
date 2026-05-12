import requests
from bs4 import BeautifulSoup

def fetch(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        p_texts = [p.get_text(strip=True) for p in soup.find_all("p")]
        return "\n".join(p_texts)
    except Exception as e:
        return f"Error: {str(e)}"
