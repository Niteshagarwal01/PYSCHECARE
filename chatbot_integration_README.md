# Mental Health Chatbot Integration

This integration allows you to use the Mental Health Chatbot functionality within the main TherapEase project.

## Setup Instructions

1. Make sure you have all the required dependencies installed:
   ```bash
   pip install nltk spacy keras tensorflow transformers spacy-langdetect
   python -m spacy download en_core_web_sm
   ```

2. Ensure the Mental-health-Chatbot-master folder is located within the TherapEase_mental-health-support-main directory.

3. The necessary model files (`model.h5`, `intents.json`, `texts.pkl`, and `labels.pkl`) should be available in the Mental-health-Chatbot-master directory.

## Usage

To use the chatbot in your project, import the functionality from the integration module:

```python
from chatbot_integration import get_chatbot_response

# Get a response from the chatbot
response = get_chatbot_response("I'm feeling anxious today")
print(response)
```

The integration supports multiple languages and will automatically detect and handle English and Swahili inputs.

## Example

Run the example file to see the chatbot in action:

```bash
python example_chatbot_usage.py
```

This will start an interactive session with the chatbot.
