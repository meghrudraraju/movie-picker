import requests
import json

API_KEY = "d5fd6f3d20a1926174b3d79165e2285f"  # replace this with your TMDB key


BASE_URL = "https://api.themoviedb.org/3"

params = {
    "api_key": API_KEY,
    "sort_by": "popularity.desc",
    "language": "en-US",
    "page": 1,
    "vote_average.gte": 7,
}

response = requests.get(f"{BASE_URL}/movie/popular", params=params)
data = response.json()

# Save to local JSON
with open("popular_movies_page1.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved movie data to popular_movies_page1.json")
