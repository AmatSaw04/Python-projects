
from bs4 import BeautifulSoup
import requests

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
all_movies = soup.find_all(name="strong")
movie_titles = [movie.getText() for movie in all_movies]
movies = movie_titles[::-1]
with open("movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")