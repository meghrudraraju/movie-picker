import os
import json
from sentence_transformers import SentenceTransformer

input_dir = "movie_features"
output_dir = "movie_vectors"
os.makedirs(output_dir, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, fast, 384-dim

for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"vectors_{filename}")

        with open(input_path, "r") as infile:
            movies = json.load(infile)

        movie_vectors = []
        for movie in movies:
            vector = model.encode(movie["feature_string"]).tolist()
            movie_vectors.append({
                "id": movie["id"],
                "title": movie["title"],
                "vector": vector
            })

        with open(output_path, "w") as outfile:
            json.dump(movie_vectors, outfile, indent=2)

        print(f"✅ Vectors written to {output_path}")
