from flask import Flask, render_template, request
import pymysql
import unicodedata
import re

app = Flask(__name__, static_url_path='/therandalbumizer/static')
application = app
app.config['APPLICATION_ROOT'] = '/therandalbumizer'

# Mapping for clean headers
COLUMN_LABELS = {
    'albumname': 'Album Name',
    'artist': 'Artist',
    'yearofrelease': 'Year of Release',
    'genres': 'Genres'
}

# --- Text cleaning function for mishandled data ---
def clean_text(text):
    if not isinstance(text, str):
        return text  # If not a string, just return it as-is

    # Normalize unicode 
    text = unicodedata.normalize('NFKC', text)

    # Replace '?' between word characters with a hyphen
    text = re.sub(r'(?<=\w)\?(?=\w)', '-', text)

    # Remove any leftover standalone question marks
    text = re.sub(r'\?+', '', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

def get_random_albums(table, count, start_year, end_year):
    connection = pymysql.connect(
        host='localhost',
        user='benjvfxw_rand_albumize',
        password='732!4dd$7993bifhd111',
        database='benjvfxw_therandalbumizer'
    )
    with connection.cursor() as cursor:
        allowed_tables = [
            'electronicalbum_data_master',
            'metalalbum_data_master',
            'altrockalbum_data_master',
            'randbalbum_data_master',
            'folkalbum_data_master'
        ]

        if table not in allowed_tables:
            table = 'electronicalbum_data_master'

        count = int(count) if count else 5

        query = f"SELECT * FROM `{table}` WHERE `yearofrelease` BETWEEN {start_year} AND {end_year} ORDER BY RAND() LIMIT {count}"
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        albums = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    connection.close()

    # --- Clean the text fields ---
    for album in albums:
        if 'albumname' in album:
            album['albumname'] = clean_text(album['albumname'])
        if 'artist' in album:
            album['artist'] = clean_text(album['artist'])
        if 'genres' in album:
            album['genres'] = clean_text(album['genres']) 

    return columns, albums

@app.route('/therandalbumizer/randalbumizer')
def home():
    return render_template('home.html')

@app.route('/randalbumizer')
def index():
    table = request.args.get('table', 'electronicalbum_data_master')
    album_count = request.args.get('album_count', 5)
    start_year = request.args.get('start_year', 1900)
    end_year = request.args.get('end_year', 2099)
    columns, albums = get_random_albums(table, album_count, start_year, end_year)

    # Column cleaning for table headers
    pretty_columns = [COLUMN_LABELS.get(col, col.title()) for col in columns]

    return render_template(
        'index.html',
        columns=columns,
        pretty_columns=pretty_columns,
        albums=albums,
        table=table,
        album_count=album_count,
        start_year=start_year,
        end_year=end_year
    )

if __name__ == '__main__':
    app.run(debug=True)
