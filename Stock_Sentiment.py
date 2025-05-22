import tkinter as tk
from tkinter import scrolledtext, ttk
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import re
from tkinter import messagebox
import threading
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def search_articles():
    query = entry.get()
    
    # Get the date filter value
    date_option = date_filter.get()
    
    # Calculate the start date based on the selected option
    if date_option == "Last 24 hours":
        start_date = datetime.now() - timedelta(days=1)
    elif date_option == "Last week":
        start_date = datetime.now() - timedelta(weeks=1)
    elif date_option == "Last month":
        start_date = datetime.now() - timedelta(days=30)
    elif date_option == "Custom date" and custom_date.get():
        try:
            start_date = datetime.strptime(custom_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date format (YYYY-MM-DD)")
            return
    else:
        start_date = None  # No date filtering
    
    # Start the search in a separate thread
    search_thread = threading.Thread(target=perform_search, args=(query, start_date))
    search_thread.daemon = True
    search_thread.start()
    
    # Show loading message
    status_label.config(text="Searching for articles...")
    search_button.config(state=tk.DISABLED)  # Disable the button during search

def perform_search(query, start_date):
    url = f"https://www.bing.com/news/search?q={query}"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        items = soup.find_all('a', {'class': 'title'})
        
        for i, item in enumerate(items):
            # Update status for each article being processed
            root.after(0, lambda msg=f"Processing article {i+1} of {len(items)}...": status_label.config(text=msg))
            
            title = item.get_text()
            link = item['href']
            
            # Try to extract article date
            article_date = extract_article_date(item, link)
            
            # Apply date filter if we have both a start date and an article date
            if start_date and article_date:
                if article_date < start_date:
                    continue  # Skip this article as it's older than the start date
            
            # Fetch article content
            article_content = fetch_article_content(link)
            
            # Create a preview (first few paragraphs)
            content_preview = create_content_preview(article_content)
            
            # Perform sentiment analysis on the article content
            sentiment_scores = analyze_sentiment(article_content, title)
            
            results.append((title, link, article_content, content_preview, article_date, sentiment_scores))
        
        save_to_csv(results)
        
        # Update UI in the main thread
        root.after(0, lambda: display_results(results))
        root.after(0, lambda: search_button.config(state=tk.NORMAL))
        root.after(0, lambda: status_label.config(text="Search complete"))
        
    except Exception as e:
        root.after(0, lambda: status_label.config(text=f"Error: {str(e)}"))
        root.after(0, lambda: search_button.config(state=tk.NORMAL))

def extract_article_date(item, url):
    """
    Try to extract the date from the article.
    First look near the article link in the search results,
    then try to scrape it from the article page if needed.
    """
    try:
        # First try to find date in search results
        parent = item.parent
        date_text = None
        
        # Look for date text in nearby elements
        for sibling in parent.find_all_next(limit=3):
            text = sibling.get_text().strip()
            if any(time_indicator in text.lower() for time_indicator in 
                  ['hour', 'day', 'minute', 'week', 'month', 'ago', 'yesterday']):
                date_text = text
                break
        
        if date_text:
            # Parse relative dates like "2 days ago", "4 hours ago", etc.
            current_date = datetime.now()
            
            if 'hour' in date_text.lower():
                hours = int(re.search(r'(\d+)\s*hour', date_text.lower()).group(1))
                return current_date - timedelta(hours=hours)
            elif 'day' in date_text.lower():
                days = int(re.search(r'(\d+)\s*day', date_text.lower()).group(1))
                return current_date - timedelta(days=days)
            elif 'week' in date_text.lower():
                weeks = int(re.search(r'(\d+)\s*week', date_text.lower()).group(1))
                return current_date - timedelta(weeks=weeks)
            elif 'month' in date_text.lower():
                months = int(re.search(r'(\d+)\s*month', date_text.lower()).group(1))
                return current_date - timedelta(days=30*months)  # Approximation
            elif 'yesterday' in date_text.lower():
                return current_date - timedelta(days=1)
        
        # If we couldn't find a date in the search results, try getting it from the article page
        response = requests.get(url, timeout=5)  # Add timeout to prevent hanging
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for common date formats in metadata
        meta_date = None
        for meta in soup.find_all('meta'):
            if meta.get('property') in ['article:published_time', 'og:published_time', 'publication_date']:
                meta_date = meta.get('content')
                break
            
        if meta_date:
            return datetime.fromisoformat(meta_date.split('T')[0])
        
        # If still no date found, return None
        return None
            
    except Exception as e:
        print(f"Error extracting date: {e}")
        return None

def fetch_article_content(url):
    """
    Fetch article content from the URL, improving extraction for more reliable content retrieval.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple approaches to find the main content
        article_content = ""
        
        # Approach 1: Look for article or main content tags
        main_content = soup.find(['article', 'main', 'div'], class_=lambda c: c and any(x in str(c).lower() for x in ['article', 'content', 'story', 'body']))
        if main_content:
            paragraphs = main_content.find_all('p')
            if paragraphs:
                article_content = ' '.join([para.get_text().strip() for para in paragraphs])
        
        # Approach 2: If no specific container found, get all paragraphs
        if not article_content:
            # Filter out very short paragraphs and navigation/cookie related text
            paragraphs = soup.find_all('p')
            filtered_paragraphs = [p.get_text().strip() for p in paragraphs 
                                   if len(p.get_text().strip()) > 40 
                                   and not any(x in p.get_text().lower() for x in ['cookie', 'privacy', 'sign up', 'subscribe'])]
            
            if filtered_paragraphs:
                article_content = ' '.join(filtered_paragraphs)
        
        # If still no content, use all paragraphs as a fallback
        if not article_content:
            all_paragraphs = soup.find_all('p')
            article_content = ' '.join([para.get_text().strip() for para in all_paragraphs])
        
        # Clean up the content
        article_content = re.sub(r'\s+', ' ', article_content).strip()
        
        return article_content
    except Exception as e:
        return f"Error fetching article: {e}"

def analyze_sentiment(content, title):
    """
    Analyze the sentiment of the article content using both TextBlob and VADER.
    Returns a dictionary with sentiment scores.
    """
    if not content or content.startswith("Error fetching article"):
        return {
            "textblob": {
                "sentiment": "NEUTRAL",
                "polarity": 0.0,
                "subjectivity": 0.0
            },
            "vader": {
                "sentiment": "NEUTRAL", 
                "compound": 0.0,
                "pos": 0.0,
                "neg": 0.0,
                "neu": 0.0
            }
        }
    
    # Combine title and content with heavier weight on title
    analysis_text = f"{title} {title} {content}"
    
    # TextBlob sentiment analysis
    blob = TextBlob(analysis_text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine TextBlob sentiment label
    if polarity > 0.1:
        textblob_sentiment = "POSITIVE"
    elif polarity < -0.1:
        textblob_sentiment = "NEGATIVE"
    else:
        textblob_sentiment = "NEUTRAL"
    
    # VADER sentiment analysis
    try:
        sid = SentimentIntensityAnalyzer()
        vader_scores = sid.polarity_scores(analysis_text)
        
        # Determine VADER sentiment label
        if vader_scores['compound'] >= 0.05:
            vader_sentiment = "POSITIVE"
        elif vader_scores['compound'] <= -0.05:
            vader_sentiment = "NEGATIVE"
        else:
            vader_sentiment = "NEUTRAL"
    except:
        # Fallback if VADER fails
        vader_sentiment = "NEUTRAL"
        vader_scores = {'compound': 0.0, 'pos': 0.0, 'neg': 0.0, 'neu': 0.0}
    
    return {
        "textblob": {
            "sentiment": textblob_sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity
        },
        "vader": {
            "sentiment": vader_sentiment, 
            "compound": vader_scores['compound'],
            "pos": vader_scores['pos'],
            "neg": vader_scores['neg'],
            "neu": vader_scores['neu']
        }
    }

def create_content_preview(content, max_length=500):
    """
    Create a preview of the article content.
    Returns first few paragraphs or sentences up to max_length characters.
    """
    if not content or content.startswith("Error fetching article"):
        return "Preview not available"
    
    # Split into sentences and build preview
    sentences = re.split(r'(?<=[.!?])\s+', content)
    preview = ""
    
    for sentence in sentences:
        if len(preview) + len(sentence) <= max_length:
            preview += sentence + " "
        else:
            break
    
    if len(content) > max_length:
        preview += "..."
    
    return preview.strip()

def save_to_csv(results):
    with open('articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'URL', 'Content', 'Date', 'TextBlob Sentiment', 'TextBlob Polarity', 'VADER Sentiment', 'VADER Compound'])
        for title, link, content, _, date, sentiment in results:
            date_str = date.strftime("%Y-%m-%d") if date else "Unknown"
            writer.writerow([
                title, 
                link, 
                content, 
                date_str, 
                sentiment["textblob"]["sentiment"], 
                sentiment["textblob"]["polarity"],
                sentiment["vader"]["sentiment"],
                sentiment["vader"]["compound"]
            ])

def display_results(results):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    
    global article_data
    article_data = results
    
    # Get the selected sentiment filter
    selected_sentiment = sentiment_filter_var.get()
    
    # Filter articles based on sentiment if a specific sentiment is selected
    filtered_results = []
    for article in results:
        title, link, _, preview, date, sentiment = article
        
        # Get sentiment information
        textblob_sentiment = sentiment["textblob"]["sentiment"]
        vader_sentiment = sentiment["vader"]["sentiment"]
        
        # Determine the overall sentiment based on both analyzers
        if textblob_sentiment == "POSITIVE" and vader_sentiment == "POSITIVE":
            overall_sentiment = "POSITIVE"
        elif textblob_sentiment == "NEGATIVE" and vader_sentiment == "NEGATIVE":
            overall_sentiment = "NEGATIVE"
        else:
            overall_sentiment = "NEUTRAL"
        
        # If "All" is selected or the article matches the selected sentiment
        if selected_sentiment == "All" or selected_sentiment == overall_sentiment:
            filtered_results.append(article)
    
    # If no articles match the filter, show a message
    if not filtered_results:
        text_area.insert(tk.END, f"No articles found with {selected_sentiment.lower()} sentiment.")
        count_label.config(text=f"Total Articles Found: 0 (Filtered from {len(results)})")
        text_area.config(state=tk.DISABLED)
        return
    
    # Display the filtered results
    for i, (title, link, _, preview, date, sentiment) in enumerate(filtered_results):
        date_str = date.strftime("%Y-%m-%d") if date else "Unknown date"
        
        # Get sentiment information
        textblob_sentiment = sentiment["textblob"]["sentiment"]
        textblob_polarity = sentiment["textblob"]["polarity"]
        vader_sentiment = sentiment["vader"]["sentiment"]
        vader_compound = sentiment["vader"]["compound"]
        
        # Determine the background color based on sentiment
        if textblob_sentiment == "POSITIVE" and vader_sentiment == "POSITIVE":
            sentiment_tag = "positive"
        elif textblob_sentiment == "NEGATIVE" and vader_sentiment == "NEGATIVE":
            sentiment_tag = "negative"
        else:
            sentiment_tag = "neutral"
        
        # Make title bold by using tags
        text_area.insert(tk.END, f"{i+1}. ", "index")
        text_area.insert(tk.END, f"{title}\n", "title")
        text_area.insert(tk.END, f"URL: {link}\n", "url")
        text_area.insert(tk.END, f"Date: {date_str}\n", "date")
        
        # Display sentiment information
        text_area.insert(tk.END, f"Sentiment: ", "sentiment_label")
        text_area.insert(tk.END, f"{textblob_sentiment}", sentiment_tag.lower())
        text_area.insert(tk.END, f" (TextBlob: {textblob_polarity:.2f}, VADER: {vader_compound:.2f})\n", "sentiment_score")
        
        # Add the preview
        if display_preview_var.get():
            text_area.insert(tk.END, f"Preview: {preview}\n", "preview")
        
        # Add buttons to view content
        view_button = tk.Button(text_area, text="View Full Article", 
                                command=lambda idx=i: show_article_content(idx))
        text_area.window_create(tk.END, window=view_button)
        
        text_area.insert(tk.END, "\n\n")
    
    # Configure tags
    text_area.tag_configure("title", font=("Arial", 13, "bold"))
    text_area.tag_configure("url", font=("Arial", 11, "italic"))
    text_area.tag_configure("date", font=("Arial", 11))
    text_area.tag_configure("preview", font=("Arial", 12))
    text_area.tag_configure("index", font=("Arial", 12, "bold"))
    text_area.tag_configure("sentiment_label", font=("Arial", 12, "bold"))
    text_area.tag_configure("sentiment_score", font=("Arial", 11))
    text_area.tag_configure("positive", foreground="green")
    text_area.tag_configure("negative", foreground="red")
    text_area.tag_configure("neutral", foreground="gray")
    
    text_area.config(state=tk.DISABLED)
    
    # Update the total number of articles found
    count_label.config(text=f"Total Articles Found: {len(filtered_results)} (Filtered from {len(results)})")

def show_article_content(article_index):
    """
    Display the full article content in a new window.
    """
    # Get the filtered results based on current sentiment filter
    selected_sentiment = sentiment_filter_var.get()
    filtered_results = []
    
    for article in article_data:
        title, link, _, preview, date, sentiment = article
        textblob_sentiment = sentiment["textblob"]["sentiment"]
        vader_sentiment = sentiment["vader"]["sentiment"]
        
        # Determine the overall sentiment based on both analyzers
        if textblob_sentiment == "POSITIVE" and vader_sentiment == "POSITIVE":
            overall_sentiment = "POSITIVE"
        elif textblob_sentiment == "NEGATIVE" and vader_sentiment == "NEGATIVE":
            overall_sentiment = "NEGATIVE"
        else:
            overall_sentiment = "NEUTRAL"
        
        # Filter based on the overall sentiment or show all if "All" is selected
        if selected_sentiment == "All" or selected_sentiment == overall_sentiment:
            filtered_results.append(article)
    
    if 0 <= article_index < len(filtered_results):
        title, link, content, _, date, sentiment = filtered_results[article_index]
        
        # Create a new window
        article_window = tk.Toplevel(root)
        article_window.title(f"Article: {title[:50]}...")
        article_window.geometry("800x600")
        
        # Add a frame for the content
        frame = tk.Frame(article_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add title and date
        title_label = tk.Label(frame, text=title, font=("Arial", 14, "bold"), wraplength=780)
        title_label.pack(anchor="w", pady=(0, 10))
        
        date_str = date.strftime("%Y-%m-%d") if date else "Unknown date"
        date_label = tk.Label(frame, text=f"Published: {date_str}", font=("Arial", 10, "italic"))
        date_label.pack(anchor="w")
        
        # Add sentiment analysis results
        textblob_sentiment = sentiment["textblob"]["sentiment"]
        textblob_polarity = sentiment["textblob"]["polarity"]
        textblob_subjectivity = sentiment["textblob"]["subjectivity"]
        vader_sentiment = sentiment["vader"]["sentiment"]
        vader_compound = sentiment["vader"]["compound"]
        
        # Set sentiment color
        if textblob_sentiment == "POSITIVE" and vader_sentiment == "POSITIVE":
            sentiment_color = "green"
        elif textblob_sentiment == "NEGATIVE" and vader_sentiment == "NEGATIVE":
            sentiment_color = "red"
        else:
            sentiment_color = "gray"
        
        sentiment_label = tk.Label(frame, text="Sentiment Analysis:", font=("Arial", 11, "bold"))
        sentiment_label.pack(anchor="w", pady=(5, 0))
        
        sentiment_frame = tk.Frame(frame)
        sentiment_frame.pack(anchor="w", pady=(0, 10), fill="x")
        
        # TextBlob results
        textblob_frame = tk.LabelFrame(sentiment_frame, text="TextBlob Analysis", padx=5, pady=5)
        textblob_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(textblob_frame, text=f"Overall: {textblob_sentiment}", 
                 font=("Arial", 9, "bold"), fg=sentiment_color).pack(anchor="w")
        tk.Label(textblob_frame, text=f"Polarity: {textblob_polarity:.2f} (-1 to +1)", 
                 font=("Arial", 9)).pack(anchor="w")
        tk.Label(textblob_frame, text=f"Subjectivity: {textblob_subjectivity:.2f} (0 to 1)", 
                 font=("Arial", 9)).pack(anchor="w")
        
        # VADER results
        vader_frame = tk.LabelFrame(sentiment_frame, text="VADER Analysis", padx=5, pady=5)
        vader_frame.pack(side=tk.LEFT)
        
        tk.Label(vader_frame, text=f"Overall: {vader_sentiment}", 
                 font=("Arial", 10, "bold"), fg=sentiment_color).pack(anchor="w")
        tk.Label(vader_frame, text=f"Compound: {vader_compound:.2f} (-1 to +1)", 
                 font=("Arial", 10)).pack(anchor="w")
        tk.Label(vader_frame, text=f"Positive: {sentiment['vader']['pos']:.2f}", 
                 font=("Arial", 10)).pack(anchor="w")
        tk.Label(vader_frame, text=f"Negative: {sentiment['vader']['neg']:.2f}", 
                 font=("Arial", 10)).pack(anchor="w")
        tk.Label(vader_frame, text=f"Neutral: {sentiment['vader']['neu']:.2f}", 
                 font=("Arial", 10)).pack(anchor="w")
        
        # Add source link
        link_label = tk.Label(frame, text=f"Source: {link}", font=("Arial", 10), foreground="blue")
        link_label.pack(anchor="w", pady=(0, 10))
        
        # Add content in a scrolled text area
        content_label = tk.Label(frame, text="Article Content:", font=("Arial", 14, "bold"))
        content_label.pack(anchor="w")
        
        content_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Arial", 14))
        content_area.pack(fill=tk.BOTH, expand=True)
        
        # Format and insert the content with better paragraph separation
        formatted_content = format_article_content(content)
        content_area.insert(tk.END, formatted_content)
        content_area.config(state=tk.DISABLED)

def format_article_content(content):
    """
    Format the article content for better readability.
    Ensures proper paragraph breaks and removes excessive whitespace.
    """
    if content.startswith("Error fetching article"):
        return content
    
    # Normalize line breaks
    content = re.sub(r'\n+', '\n', content)
    
    # Split into paragraphs (sentences that end with periods)
    paragraphs = []
    current_para = ""
    
    for sentence in re.split(r'(?<=[.!?])\s+', content):
        if len(current_para) > 0:
            current_para += " " + sentence
        else:
            current_para = sentence
            
        # Start a new paragraph after ~3-5 sentences or if it's already long
        if current_para.count('.') >= 3 or len(current_para) > 500:
            paragraphs.append(current_para)
            current_para = ""
    
    # Add the last paragraph if it's not empty
    if current_para:
        paragraphs.append(current_para)
    
    # Join paragraphs with double line breaks
    formatted_text = "\n\n".join(paragraphs)
    
    return formatted_text

def update_custom_date_entry(*args):
    if date_filter.get() == "Custom date":
        custom_date_entry.config(state="normal")
    else:
        custom_date_entry.config(state="disabled")

# Global variable to store article data
article_data = []

root = tk.Tk()
root.title("Web Article Search & Sentiment Analysis")

# Create a main frame to hold everything
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Search frame
search_frame = tk.Frame(main_frame)
search_frame.pack(fill=tk.X, padx=5, pady=5)

label = tk.Label(search_frame, text="Enter search term:")
label.grid(row=0, column=0, sticky="w")

entry = tk.Entry(search_frame, width=50)
entry.grid(row=0, column=1, padx=5, sticky="w")

# Date filter options
date_filter_frame = tk.Frame(search_frame)
date_filter_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

date_label = tk.Label(date_filter_frame, text="Date filter:")
date_label.grid(row=0, column=0, sticky="w")

date_filter = tk.StringVar()
date_filter.set("No date filter")  # Default value
date_options = ["No date filter", "Last 24 hours", "Last week", "Last month", "Custom date"]
date_dropdown = ttk.Combobox(date_filter_frame, textvariable=date_filter, values=date_options, width=15)
date_dropdown.grid(row=0, column=1, padx=5, sticky="w")

# Custom date entry
custom_date = tk.StringVar()
custom_date_label = tk.Label(date_filter_frame, text="Enter date (YYYY-MM-DD):")
custom_date_label.grid(row=0, column=2, padx=5, sticky="w")
custom_date_entry = tk.Entry(date_filter_frame, textvariable=custom_date, width=12, state="disabled")
custom_date_entry.grid(row=0, column=3, padx=5, sticky="w")

# Bind the combobox change to update the custom date entry state
date_filter.trace('w', update_custom_date_entry)

# Display options
display_options_frame = tk.Frame(search_frame)
display_options_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

display_preview_var = tk.BooleanVar(value=True)
preview_checkbox = tk.Checkbutton(display_options_frame, text="Show article previews in results", 
                                  variable=display_preview_var)
preview_checkbox.pack(side=tk.LEFT, padx=5)

# Sentiment filter options
sentiment_frame = tk.LabelFrame(search_frame, text="Sentiment Filter", padx=5, pady=5)
sentiment_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

sentiment_filter_var = tk.StringVar(value="All")
tk.Radiobutton(sentiment_frame, text="All", variable=sentiment_filter_var, value="All").grid(row=0, column=0, padx=5)
tk.Radiobutton(sentiment_frame, text="Positive", variable=sentiment_filter_var, value="POSITIVE").grid(row=0, column=1, padx=5)
tk.Radiobutton(sentiment_frame, text="Neutral", variable=sentiment_filter_var, value="NEUTRAL").grid(row=0, column=2, padx=5)
tk.Radiobutton(sentiment_frame, text="Negative", variable=sentiment_filter_var, value="NEGATIVE").grid(row=0, column=3, padx=5)

# Add a button to apply the filter to current results
apply_filter_button = tk.Button(sentiment_frame, text="Apply Filter", 
                               command=lambda: display_results(article_data))
apply_filter_button.grid(row=0, column=4, padx=5)

# Search button
search_button = tk.Button(search_frame, text="Search", command=search_articles)
search_button.grid(row=4, column=0, columnspan=2, pady=10)

# Status label
status_label = tk.Label(search_frame, text="", font=("Arial", 12, "italic"))
status_label.grid(row=5, column=0, columnspan=2, sticky="w")

# Results frame
result_frame = tk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Results header
results_header = tk.Label(result_frame, text="Search Results", font=("Arial", 15, "bold"))
results_header.pack(anchor="w", pady=(0, 5))

text_area = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20)
text_area.pack(fill=tk.BOTH, expand=True)

# Results footer with count label
count_label = tk.Label(result_frame, text="Total Articles Found: 0")
count_label.pack(pady=5)

# Make the window resizable
root.geometry("900x700")
root.minsize(800, 600)

root.mainloop()
