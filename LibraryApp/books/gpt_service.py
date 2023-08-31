# books/gpt_service.py
import openai
import json
import logging

from django.conf import settings


logging.basicConfig(level=logging.INFO)

def preprocess_query(query):

    return f"I am interested in {query}. Can you suggest a books for me?"

def generate_book_suggestion(query):
    openai.api_key = settings.GPT_API_KEY

 
    custom_instruction = "You are a helpful assistant specialized in suggesting books suggest max 5 books. Please provide the suggestion in a JSON-compatible format, including fields for 'title', 'author', and 'ISBN'."

   
    processed_query = preprocess_query(query)

    messages = [
        {"role": "system", "content": custom_instruction},
        {"role": "user", "content": processed_query}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

  
    logging.info(f"GPT-3 Raw Response: {response}")

    suggestion_str = response['choices'][0]['message']['content'].strip()

    logging.info(f"Parsed Content from GPT-3: {suggestion_str}")

    try:
        suggestion_dict = json.loads(suggestion_str)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed. Error: {e}")
        suggestion_dict = {"error": "Invalid suggestion format"}

   
    if "books" in suggestion_dict and isinstance(suggestion_dict["books"], dict):
        suggestion_dict["books"] = list(suggestion_dict["books"].values())

    logging.info(f"Suggestion Dictionary: {suggestion_dict}")

    return suggestion_dict

