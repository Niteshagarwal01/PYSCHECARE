from chatbot_integration import get_chatbot_response, detect_language

def main():
    print("TherapEase Mental Health Chatbot")
    print("Type 'exit' to end the conversation")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
            
        # Get response from the chatbot
        response = get_chatbot_response(user_input)
        print(f"TherapEase: {response}")

if __name__ == "__main__":
    main()
