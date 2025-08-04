import os
import json

# Input and output directories
input_dir = "popular_movies"
output_dir = "movie_features"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Helper function to build a feature string
def build_feature_string(movie):
    title = movie.get("title", "")
    overview = movie.get("overview", "")
    language = movie.get("original_language", "")
    vote_average = str(movie.get("vote_average", ""))
    genre_ids = [str(genre_id) for genre_id in movie.get("genre_ids", [])]

    return f"{title}. {overview}. Language: {language}. Rating: {vote_average}. Genres: {' '.join(genre_ids)}"

# Process each file
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"features_{filename}")

        with open(input_path, "r") as infile:
            movies = json.load(infile)

        movie_features = []
        for movie in movies:
            movie_features.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "feature_string": build_feature_string(movie)
            })

        with open(output_path, "w") as outfile:
            json.dump(movie_features, outfile, indent=2)

        print(f"✅ Processed {len(movie_features)} movies from {filename} → {output_path}")
