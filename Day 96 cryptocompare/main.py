from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://hp-api.onrender.com/api/characters"

@app.route('/', methods=['GET'])
def index():
    # Get the search query from the URL (e.g., /?name=Harry Potter)
    name_query = request.args.get('name')
    character = None
    searched = False # This flag helps the template know if a search was attempted

    # If a name was provided in the URL, proceed with the search
    if name_query:
        searched = True
        try:
            response = requests.get(API_URL)
            # Check if the API request was successful
            if response.status_code == 200:
                characters = response.json()
                # Loop through all characters to find a match (case-insensitive)
                for c in characters:
                    if c['name'].lower() == name_query.lower():
                        character = c
                        break # Stop searching once a match is found
        except requests.exceptions.RequestException as e:
            # Handle potential network errors
            print(f"API request failed: {e}")

    # Render the HTML template, passing the found character and search status
    return render_template('index.html', character=character, searched=searched)

if __name__ == '__main__':
    app.run(debug=True)