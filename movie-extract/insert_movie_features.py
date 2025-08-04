import os
import json
from sqlalchemy.dialects.postgresql import insert
from app.db.database import SessionLocal
from app.models.movie_features import MovieFeature
from app.models.movies import Movie

# Paths for testing
FEATURE_FILE = "movie_features/features_popular_movies_9001_10000.json"
VECTOR_FILE = "movie_vectors/vectors_features_popular_movies_9001_10000.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load {path}: {e}")
        return []

def insert_features():
    session = SessionLocal()

    feature_data = load_json(FEATURE_FILE)
    vector_data = load_json(VECTOR_FILE)

    # Map TMDB ID to vector for quick lookup
    vector_map = {v["id"]: v["vector"] for v in vector_data}

    upserts = 0
    for entry in feature_data:
        tmdb_id = entry["id"]
        feature_string = entry["feature_string"]
        vector = vector_map.get(tmdb_id)

        if vector is None:
            print(f"⚠️ No vector found for TMDB ID {tmdb_id}")
            continue

        movie = session.query(Movie).filter_by(tmdb_id=tmdb_id).first()
        if not movie:
            print(f"⚠️ Movie not found for TMDB ID {tmdb_id}")
            continue

        stmt = insert(MovieFeature).values(
            tmdb_id=tmdb_id,
            feature_string=feature_string,
            vector=vector
        ).on_conflict_do_update(
            index_elements=["tmdb_id"],
            set_={
                "feature_string": feature_string,
                "vector": vector
            }
        )

        session.execute(stmt)
        upserts += 1

    try:
        session.commit()
        print(f"✅ Upserted {upserts} feature entries")
    except Exception as e:
        session.rollback()
        print(f"❌ Commit failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_features()
