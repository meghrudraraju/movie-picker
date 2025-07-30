import sys
import requests
API_KEY = "d5fd6f3d20a1926174b3d79165e2285f"  #API KEY
BASE_URL = "https://api.themoviedb.org/3"
def parse_args(arg_list):
    # First: split any comma-separated items into individual strings
    expanded = []
    for item in arg_list:
        expanded.extend(item.split(','))
    # Then parse key:value as before
    result = {}
    for arg in expanded:
        if ':' not in arg:
            print(f"Bad format (expected key:value): {arg}", file=sys.stderr)
            sys.exit(1)
        key, val = arg.split(':', 1)
        result[key.lower()] = val
    return result

#def main():
    # step 1: grab everything after the script name
    #raw_args = sys.argv[1:]
    
    # step 2: parse (and expand commas)
    #args = parse_args(raw_args)
    
    # step 3: pull into individual variables
    #genre      = args.get('genre')
    #movies     = args.get('Movies')      or args.get('movies')
    #preference = args.get('Preference')  or args.get('preference')
    
    #print(f"Genre      = ",genre)
    #print(f"Movies     = ",movies)
    #print(f"Preference = ",preference)

#if __name__ == "__main__":
#    main()


# ---------------------- Scenario Detection ----------------------
def determine_scenario(args):
    """Determine which recommendation scenario applies."""
    has_genre = 'genre' in args
    has_movies = 'movies' in args
    has_pref = 'preference' in args
    if has_genre and not has_movies and not has_pref:
        return 'genre_only'
    if has_genre and has_pref and not has_movies:
        return 'genre_pref'
    if has_genre and has_movies and not has_pref:
        return 'genre_movies'
    if has_genre and has_movies and has_pref:
        return 'genre_movies_pref'
    return 'invalid'

def fetch_movies_by_genre_id(genre_id):
    """Fetch movies using the discover endpoint with a numeric genre_id."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        # you can add default sorting here, e.g. "sort_by": "popularity.desc"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("results", [])

# ---------------------- Business Logic ----------------------
def recommend(args):
    scenario = determine_scenario(args)
    genre = args.get('genre')
    movies = args.get('movies')
    preference = args.get('preference')
    if scenario == 'genre_only':
        print("Scenario: Only Genre")
        candidates = fetch_movies_by_genre(genre)
        return sorted(candidates, key=lambda m: m.get('vote_average', 0), reverse=True)

    if scenario == 'genre_pref':
        print("Scenario: Genre + Preference")
        candidates = fetch_movies_by_genre(genre)
        key = 'vote_average'
        if preference.lower() == 'popularity': key = 'popularity'
        elif preference.lower() == 'new': key = 'release_date'
        return sorted(candidates, key=lambda m: m.get(key, 0), reverse=True)

    if scenario == 'genre_movies':
        print("Scenario: Genre + Movies")
        movie_id = fetch_movie_id(movies)
        recs = fetch_recommendations(movie_id)
        filtered = [m for m in recs if genre.lower() in [g.lower() for g in m.get('genre_ids', [])]]
        return sorted(filtered, key=lambda m: m.get('vote_average', 0), reverse=True)

    if scenario == 'genre_movies_pref':
        print("Scenario: Genre + Movies + Preference")
        movie_id = fetch_movie_id(movies)
        recs = fetch_recommendations(movie_id)
        filtered = [m for m in recs if genre.lower() in [g.lower() for g in m.get('genre_ids', [])]]
        key = 'vote_average'
        if preference.lower() == 'popularity': key = 'popularity'
        elif preference.lower() == 'new': key = 'release_date'
        return sorted(filtered, key=lambda m: m.get(key, 0), reverse=True)

    print("Invalid or insufficient arguments. Expected at least 'genre'.")
    return []


def main():
    # step 1: grab everything after the script name
    raw_args = sys.argv[1:]
    
    # step 2: parse (and expand commas)
    args = parse_args(raw_args)

    scenario = determine_scenario(args)
    print(f"Current Scenario is ",scenario)

if __name__ == '__main__':
    main()
