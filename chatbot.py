import csv
import string
import os

FAQ_FILE = 'faq.csv'

# Load FAQ data
def load_faq():
    faq_data = []
    if os.path.exists(FAQ_FILE):
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                faq_data.append({'question': row['Question'], 'answer': row['Answer']})
    return faq_data

# Save new FAQ
def save_faq(question, answer):
    file_exists = os.path.exists(FAQ_FILE)
    with open(FAQ_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Question', 'Answer'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'Question': question, 'Answer': answer})

# Preprocess text
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Simple string similarity
def simple_similarity(user_input, question):
    user_words = set(user_input.split())
    question_words = set(question.split())
    if not question_words:
        return 0
    return len(user_words & question_words) / len(question_words) * 100

def get_answer(user_input, faq_data):
    user_input_proc = preprocess(user_input)
    max_score = 0
    answer = None
    
    for item in faq_data:
        question_proc = preprocess(item['question'])
        score = simple_similarity(user_input_proc, question_proc)
        if score > max_score and score >= 40:
            max_score = score
            answer = item['answer']
    return answer

# Chatbot main loop
def chatbot():
    faq_data = load_faq()
    print("Chatbot: Hello! You can ask a question, or type 'exit' to quit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        elif user_input.lower() in ['hi', 'hello', 'hey', 'good morning', 'good evening']:
            print("Chatbot: Hello! How can I help you?")
        else:
            answer = get_answer(user_input, faq_data)
            if answer:
                print("Chatbot:", answer)
            else:
                print("Chatbot: I don't know the answer to that question.")
                teach = input("Would you like to teach me the answer? (yes/no): ").strip().lower()
                if teach in ['yes', 'y']:
                    new_answer = input("Enter the answer: ").strip()
                    save_faq(user_input, new_answer)
                    faq_data = load_faq()  # reload updated data
                    print("Chatbot: Thanks! I've learned a new answer.")

if __name__ == "__main__":
    chatbot()
