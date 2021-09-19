import requests

def run_quickstart(tweets):
    # Imports the Google Cloud client library
    from google.cloud import language_v1

    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    sentimentScore = []
    sentimentMagnitude = []

    # Loop 
    for x in range(len(tweets)):

        # The text to analyze
        text = tweets[x]
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

        sentimentScore.append(round((1 + sentiment.score) / 2, 2))
        sentimentMagnitude.append(round(sentiment.magnitude, 2))
        
    return sentimentScore, sentimentMagnitude


if __name__ == "__main__":
    #temporary placeholder text, tweets will be provided by Twitter scrapper and tweets, sentimentScore, sentimentMagnitude, Platform, Query will 
    # all be passed forward to Cockroach Database
    fb_tweets = ["Facebook is terrible"]
    tweets = ["Hello everyone!. This is interesting", "I love this world", "Pancakes are ok i guess...", "I am livid, I hate this. I am filled with anger"]
    sentimentScore, sentimentMagnitude = run_quickstart(tweets)
    print(tweets)
    print(sentimentScore)
    print(sentimentMagnitude)

    # --------------- GENERATING DEMO DATA HERE ---------------

    # POST search terms if they haven't already been POSTed
    demoSearchTerms = ["Facebook", "Hack the North", "Justin Trudeau"]
    for st in demoSearchTerms:
        response = requests.get("http://0.0.0.0:8000/searchTerms/" + st + "/")
        if response.status_code != 200: 
            requests.post("http://0.0.0.0:8000/searchTerms/" + st + "/", data = {
                "name": st,
                "sentiment_score_v1": 0.0
            })

    # POST social media posts 
    for i in range(0, 4, 1):
        response = requests.post("http://0.0.0.0:8000/socialMediaPosts/", data = {
            "content": tweets[i],
            "sentiment": sentimentScore[i],
            "search_term": "facebook"
        })

    # PATCH search terms to calculated sentiment score values
    requests.patch("http://0.0.0.0:8000/searchTerms/Facebook/", data = {
        "sentiment_score_v1": 0.2
    })
    requests.patch("http://0.0.0.0:8000/searchTerms/Hack the North/", data = {
        "sentiment_score_v1": 1.0
    })
    requests.patch("http://0.0.0.0:8000/searchTerms/Justin Trudeau/", data = {
        "sentiment_score_v1": 0.5
    })
    