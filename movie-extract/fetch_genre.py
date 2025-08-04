import requests
import json

TMDB_API_KEY = "d5fd6f3d20a1926174b3d79165e2285f"  # Replace if needed
GENRE_URL = f"https://api.themoviedb.org/3/genre/movie/list"

params = {
    "api_key": TMDB_API_KEY,
    "language": "en-US"
}

try:
    response = requests.get(GENRE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    with open("genres.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Fetched and saved {len(data['genres'])} genres to genres.json")

except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching genres: {e}")
