from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Mapping for clean headers
COLUMN_LABELS = {
    'albumname': 'Album Name',
    'artist': 'Artist',
    'yearofrelease': 'Year of Release',
    'genres': 'Genres'
}

def get_random_albums(table, count, start_year, end_year):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
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
    return columns, albums

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/randalbumizer')
def index():
    table = request.args.get('table', 'electronicalbum_data_master')
    album_count = request.args.get('album_count', 5)
    start_year = request.args.get('start_year', 1900)
    end_year = request.args.get('end_year', 2099)
    columns, albums = get_random_albums(table, album_count, start_year, end_year)

    # Column cleaning
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
