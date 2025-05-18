from flask import Flask, render_template, request, send_from_directory
import os
from utils.rss_parser import parse_rss_feed
from utils.summarizer import summarize_article
from utils.infographic import generate_infographic

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/infographics'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rss_url = request.form['rss_url']
        try:
            # Parse RSS feed
            articles = parse_rss_feed(rss_url)
            if not articles:
                return render_template('index.html', error="No articles found in the RSS feed.")
            
            # Process the first article
            article = articles[0]
            title, summary = summarize_article(article['link'])
            
            # Generate infographic
            infographic_path = generate_infographic(title, summary)
            infographic_filename = os.path.basename(infographic_path)
            
            return render_template('result.html', infographic=infographic_filename)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/infographics/<filename>')
def serve_infographic(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)