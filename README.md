# Artigraphics
A Python web app to generate infographics from RSS feeds and web articles.

## Features
- Fetches articles from RSS feeds using `feedparser`.
- Summarizes articles using `newspaper3k` and `nltk`.
- Generates infographics with wrapped text and word clouds using `cairosvg`, `Pillow`, and `matplotlib`.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Artigraphics.git
   cd Artigraphics

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Download NLTK data for summarization:
    ```bash
    python -m nltk.downloader punkt punkt_tab

## Usage
    Run the Flask app:
    ```bash
    python app.py

* Open your browser and go to http://127.0.0.1:5000.

* Enter an RSS feed URL (e.g., http://feeds.bbci.co.uk/news/rss.xml) and submit.

* View and download the generated infographic.

## Notes
* Ensure you have Python 3.12 or later installed.

* The app generates infographics in static/infographics/, which are excluded from Git via .gitignore.

* For debugging, check static/debug.svg to inspect the raw SVG template.




