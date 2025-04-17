import sys
import os
import json
import random
import numpy as np
import nltk
import pickle
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from autocorrect import Speller

# Add the Python-Mental-Health-Chatbot-main directory to sys.path
python_chatbot_path = os.path.join(os.path.dirname(__file__), "Python-Mental-Health-Chatbot-main", "Python-Mental-Health-Chatbot-main")
sys.path.append(python_chatbot_path)

# Make sure required NLTK packages are downloaded
try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    print("NLTK packages downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK packages: {e}")

# Lemmatizer for processing text
lemmatizer = WordNetLemmatizer()

# Define global variables that will be initialized in load_chatbot_model()
words = []
classes = []
model = None
intents = {}
context = {}

def load_chatbot_model():
    """
    Load the chatbot model and necessary data files
    """
    global words, classes, model, intents
    
    try:
        # Set paths for model files
        model_path = os.path.join(python_chatbot_path, "chatbot-model.h5")
        pickle_path = os.path.join(python_chatbot_path, "data.pickle")
        intents_path = os.path.join(python_chatbot_path, "ChatbotWebsite", "static", "data", "intents.json")
        
        # Check if we're working with the provided files or the ones in the original location
        if not os.path.exists(intents_path):
            intents_path = os.path.join(os.path.dirname(__file__), "chatbot_files", "intents.json")
            model_path = os.path.join(os.path.dirname(__file__), "chatbot_files", "model.h5")
            pickle_path = os.path.join(os.path.dirname(__file__), "chatbot_files", "data.pickle")
        
        # Load intents file
        with open(intents_path) as file:
            intents = json.load(file)
        
        # Try to load existing model and data
        try:
            with open(pickle_path, "rb") as f:
                words, classes, training, output = pickle.load(f)
            model = load_model(model_path)
            print("Chatbot model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("You need to train the model first or provide the model files")
            return False
            
        return True
    
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        return False

# Helper functions from the Python chatbot implementation
def clean_up_message(message):
    """Clean and tokenize the message"""
    message_word_list = nltk.word_tokenize(message)
    message_word_list = [
        lemmatizer.lemmatize(word.lower()) for word in message_word_list
    ]
    return message_word_list

def bag_of_words(message, words_list):
    """Create a bag of words from the message"""
    message_word = clean_up_message(message)
    bag = [0] * len(words_list)
    for w in message_word:
        for i, word in enumerate(words_list):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(message, ERROR_THRESHOLD=0.25):
    """Predict the intent class of the message"""
    global words, classes, model
    
    bow = bag_of_words(message, words)
    res = model.predict(np.array([bow]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def get_chatbot_response(message, user_id="000"):
    """
    Get a response from the chatbot based on the input message.
    
    Args:
        message (str): The user's message
        user_id (str): Optional user ID for context tracking
    
    Returns:
        str: The chatbot's response
    """
    global words, classes, model, intents, context
    
    # Make sure model is loaded
    if model is None:
        success = load_chatbot_model()
        if not success:
            return "Sorry, the chatbot is not available at the moment."
    
    try:
        # Apply spelling correction
        spell = Speller()
        corrected_message = spell(message)
        
        # Get predictions
        results = predict_class(corrected_message)
        
        if results:  # if results exist
            while results:  # loop through results
                for intent in intents["intents"]:  # loop through intents
                    if intent["tag"] == results[0][0]:  # if tag matches
                        if intent["tag"].lower() == "reiterate":  # if tag is reiterate
                            if context.get(user_id):  # if context exists
                                for tg in intents["intents"]:
                                    if (
                                        "context_set" in tg
                                        and tg["context_set"] == context[user_id]
                                    ):
                                        response = random.choice(tg["responses"])
                                        return str(response)
                            else:
                                response = random.choice(intent["responses"])
                                return str(response)
                        if "context_set" in intent and intent["context_set"] != "":
                            context[user_id] = intent["context_set"]
                        response = random.choice(intent["responses"])
                        return str(response)
                results.pop(0)
        
        # Default response if no matching intent
        return "I apologize if my response wasn't what you were looking for. As an AI assistant, my knowledge is limited. Is there another way I can help you?"
    
    except Exception as e:
        print(f"Error getting chatbot response: {e}")
        return "Sorry, I'm having trouble processing your request right now."

def detect_language(text):
    """
    Detect the language of the input text.
    This is a simplified function that always returns English for now.
    
    Args:
        text (str): The input text
    
    Returns:
        str: The detected language code
    """
    return "en"  # Default to English

# Initialize the chatbot model when this module is imported
load_chatbot_model()
