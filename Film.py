
import requests
from bs4 import BeautifulSoup

# Target VOX Cinemas URL
url = "https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&m=avengers-doomsday&d=20261218"

# Add a User-Agent header to mimic a real browser request and avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the movie compare/showtimes section
    movie_section = soup.find('article', class_='movie-compare')
    
    if movie_section:
        movie_title = movie_section.find('h2').text.strip()
        print(f"Movie: {movie_title}\n")
        
        # Find cinema location header
        cinema_name = movie_section.find('h3', class_='highlight')
        print(f"Cinema: {cinema_name.text.strip() if cinema_name else 'City Centre Almaza'}\n")
        
        # Iterate through experience types (e.g., GOLD, Standard)
        showtime_blocks = movie_section.find_all('ol', class_='showtimes')
        
        for block in showtime_blocks:
            items = block.find_all('li')
            for item in items:
                experience_type = item.find('strong')
                if experience_type:
                    print(f"=== Experience: {experience_type.text.strip()} ===")
                    
                # Find individual showtime slots and their data-id attributes
                slots = item.find_all('li', {'data-id': True})
                for slot in slots:
                    slot_id = slot.get('data-id')
                    time_span = slot.find('span', class_='action showtime')
                    
                    if time_span:
                        time_text = time_text = time_span.text.strip()
                        status = "Unavailable" if "unavailable" in time_span.get('class', []) else "Available"
                        print(f"  - Showtime: {time_text} | Status: {status} | Tracking ID: {slot_id}")
        else:
            print("No showtimes found in this block.")
    else:
        print("Could not find the movie-compare section on the page.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
