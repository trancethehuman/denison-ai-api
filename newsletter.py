import json
from ai import get_openai_article_recommendation


with open("./test-data/news-the-denisonian.json", "r", encoding="utf8") as f:
    data = json.load(f)


set_the_tone = "Give me summaries of articles that I might be interested, and reasons why I should read them, in from the context I gave you. The articles have to exist in the context. Do not make up articles that aren't found in the context I gave you."


def get_news_recommendation(user_profile, context, number_of_articles):
    number_of_articles_string = f" limit to {number_of_articles} articles."
    set_the_tone_complete = f"{set_the_tone} {number_of_articles_string}"
    file_path = ""
    if (context == "denison.edu"):
        file_path = "news-denison-edu.json"

    if (context == "The Denisonian"):
        file_path = "news-the-denisonian.json"

    with open(f"./test-data/{file_path}", "r", encoding="utf8") as f:
        data = json.load(f)
        return get_openai_article_recommendation(data, user_profile, set_the_tone_complete)
