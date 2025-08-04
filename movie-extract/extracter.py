import requests
import json
import time
from requests.adapters import HTTPAdapter, Retry

API_KEY = "d5fd6f3d20a1926174b3d79165e2285f"
BASE_URL = "https://api.themoviedb.org/3/movie/popular"
TOTAL_PAGES = 50  # 20 movies per page → 1000 movies total

# Setup session with retry strategy
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

all_movies = []

for page in range(451, 501):  # Pages 101 to 150 → Next 1000 movies
    print(f"📥 Fetching page {page}...")

    params = {
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "language": "en-US",
        "page": page,
        "vote_average.gte": 7,
    }

    try:
        response = session.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        movies = data.get("results", [])
        all_movies.extend(movies)

        # Optional: throttle to avoid hitting API limits
        time.sleep(0.25)  # 4 requests per second

    except requests.RequestException as e:
        print(f"❌ Error fetching page {page}: {e}")
        break

# Save all movies to a single JSON file
with open("popular_movies_9001_10000.json", "w") as f:
    json.dump(all_movies, f, indent=2)

print(f"✅ Saved {len(all_movies)} movies to popular_movies_9001_10000.json")
