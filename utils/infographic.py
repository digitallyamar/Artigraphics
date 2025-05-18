import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from jinja2 import Environment, FileSystemLoader
import cairosvg
import io
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def wrap_text(text, max_chars_per_line=80):
    """Split text into lines with a maximum character count."""
    if not text:
        logger.warning("Empty text provided to wrap_text")
        return ["[No text available]"]
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length <= max_chars_per_line:
            current_line.append(word)
            current_length += word_length
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length
    if current_line:
        lines.append(' '.join(current_line))
    
    logger.debug(f"Wrapped text: {lines}")
    return lines

def generate_wordcloud(text):
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text or "placeholder")
    plt.figure(figsize=(4, 2))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return Image.open(buf)

def generate_infographic(title, summary):
    # Debug input
    logger.debug(f"Title: {title}")
    logger.debug(f"Summary: {summary}")
    
    # Wrap title and summary
    title_lines = wrap_text(title or "[No title]", max_chars_per_line=60)  # Shorter for title
    summary_lines = wrap_text(summary or "[No summary]", max_chars_per_line=80)

    # Load Jinja2 SVG template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('infographic.svg')
    
    # Render SVG with content
    svg_content = template.render(title_lines=title_lines, summary_lines=summary_lines)
    
    # Save SVG for debugging
    with open('static/debug.svg', 'w') as f:
        f.write(svg_content)
    
    # Convert SVG to PNG using cairosvg
    svg_buffer = io.BytesIO(svg_content.encode('utf-8'))
    png_buffer = io.BytesIO()
    try:
        cairosvg.svg2png(file_obj=svg_buffer, write_to=png_buffer, output_width=800, output_height=600)
    except Exception as e:
        logger.error(f"SVG to PNG conversion failed: {str(e)}")
        raise
    
    png_buffer.seek(0)
    
    # Open PNG and add word cloud
    infographic = Image.open(png_buffer)
    wordcloud = generate_wordcloud(summary or "placeholder")
    
    # Paste word cloud onto infographic
    wordcloud = wordcloud.resize((400, 200))
    infographic.paste(wordcloud, (200, 350))
    
    # Save infographic
    output_path = f"static/infographics/infographic_{hash(title or 'default')}.png"
    infographic.save(output_path, 'PNG')
    
    logger.debug(f"Infographic saved: {output_path}")
    return output_path