import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article
from textblob.en import sentiment
import spacy
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

openai.api_key = "your-openai-api-key"


def summarize_with_gpt(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following article: {text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()


def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def summarize():

    url = utext.get('1.0' , "end").strip()

    article = Article(url)

    article.download()
    article.parse()

    article.nlp()
    summary = summarize_with_gpt(article.text)
    entities = extract_entities(article.text)

    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    title.delete('1.0', 'end')
    title.insert('1.0', article.title)

    author.delete('1.0', 'end')
    author.insert('1.0', article.authors)

    publication.delete('1.0', 'end')
    publication.insert('1.0', str(article.publish_date))

    summary.delete('1.0', 'end')
    summary.insert('1.0', article.summary)

    analysis = TextBlob(article.text)
    sentiment.delete('1.0', 'end')
    sentiment.insert('1.0' , f'Polarity: {analysis.polarity}, Sentiment: {"positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"}')

    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')


def pipeline(param):
    pass


def summarize_with_ml(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return "Positive"
    elif sentiment_score['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"



root = tk. Tk()
root.title("News Summarizer")
root.geometry('1200x600')

tlabel = tk.Label(root, text="Title")
tlabel.pack()

title = tk. Text(root, height=1, width=140)
title.config(state='disabled', bg='#dddddd')
title.pack()

alabel = tk.Label(root, text="Author")
alabel.pack()

author = tk. Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd' )
author.pack()

plabel = tk.Label(root, text="Publishing Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd' )
publication.pack()

slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk. Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

selabel = tk.Label(root, text="Sentiment Analysis")
selabel.pack()

sentiment = tk. Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

ulabel = tk.Label(root, text="URL")
ulabel.pack()

utext = tk. Text(root, height=1, width=140)
utext.pack()

btn = tk. Button(root, text="Summarize", command=summarize)
btn.pack()

root.mainloop()