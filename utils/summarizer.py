from newspaper import Article
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def summarize_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    
    title = article.title
    summary = article.summary
    
    # Ensure summary is concise (e.g., max 3 sentences)
    sentences = sent_tokenize(summary)
    summary = ' '.join(sentences[:3])
    
    return title, summary