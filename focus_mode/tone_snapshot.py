from textblob  import TextBlob

def analyze_tone(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    tone = "Neutral"
    if polarity > 0.3:
        tone = "Positive"
    elif polarity < -0.3:
        tone = "Negative"
    
    return {
        "tone": tone,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2)
    }