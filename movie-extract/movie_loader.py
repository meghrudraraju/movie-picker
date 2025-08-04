import sys
import os
import json
import datetime
from sqlalchemy.exc import IntegrityError

# Add parent directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.db.database import SessionLocal
from app.models.movies import Movie

# Load just one test file
FILE_PATH = os.path.join("popular_movies", "popular_movies_9001_10000.json")

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def load_movies_from_file():
    session = SessionLocal()
    inserted = 0

    if not os.path.exists(FILE_PATH):
        print(f"❌ File not found: {FILE_PATH}")
        return

    with open(FILE_PATH, "r") as file:
        try:
            movies = json.load(file)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {FILE_PATH}")
            return

    for movie in movies:
        tmdb_id = movie.get("id")
        title = movie.get("title")

        if session.query(Movie).filter_by(tmdb_id=tmdb_id).first():
            print(f"⏭️ Already exists: tmdb_id={tmdb_id}")
            continue

        new_movie = Movie(
            tmdb_id=tmdb_id,
            title=title,
            original_title=movie.get("original_title"),
            original_language=movie.get("original_language"),
            overview=movie.get("overview"),
            release_date=parse_date(movie.get("release_date")),
            popularity=movie.get("popularity"),
            vote_average=movie.get("vote_average"),
            vote_count=movie.get("vote_count"),
            poster_path=movie.get("poster_path"),
            backdrop_path=movie.get("backdrop_path"),
            video=movie.get("video", False)
        )

        try:
            session.add(new_movie)
            session.commit()
            inserted += 1
        except IntegrityError:
            session.rollback()
            print(f"⚠️ Skipped duplicate tmdb_id={tmdb_id}")

    session.close()
    print(f"✅ Done! Inserted {inserted} new movies from {FILE_PATH}")

if __name__ == "__main__":
    load_movies_from_file()
