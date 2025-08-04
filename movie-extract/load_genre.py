import json
from app.db.database import SessionLocal
from app.models.genre import Genre

def load_genres_from_file(file_path="genres.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    genres = data.get("genres", [])
    session = SessionLocal()

    for genre in genres:
        genre_obj = Genre(id=genre["id"], name=genre["name"])
        session.merge(genre_obj)  # upsert to avoid duplicates
        print(f"✅ Inserted: {genre_obj.id} - {genre_obj.name}")

    session.commit()
    session.close()
    print(f"🎉 Loaded {len(genres)} genres into DB.")

if __name__ == "__main__":
    load_genres_from_file()
