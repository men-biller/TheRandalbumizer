#  The Randalbumizer

The **Randalbumizer** is a data-driven random album generator built with Python and Flask.

##  Features
- Generate a **custom number** of random albums (choose between **1–100** albums)
- Filter albums by:
  - Genre
  - Year of release range
- View clean, formatted album and artist names

##  Technologies
- Flask (Python web framework)
- MySQL (album data storage)

##  Data Sources
- 5 curated genre-specific MySQL tables
- 1,000 total albums

##  How It Works
- User selects genre, number of albums, and year range on the homepage
- Flask queries the database and randomly selects the specified number of albums
- Results are dynamically rendered on a clean, user-friendly web page
