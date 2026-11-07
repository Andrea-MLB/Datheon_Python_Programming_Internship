import json
import re

# Words that mean "leave the chat"
EXIT_WORDS = {'bye', 'exit', 'quit'}

# Filler words we ignore, because they don't tell us what the user wants
STOP_WORDS = {'is', 'the', 'a', 'an', 'do', 'i', 'how', 'what', 'are', 'your',
              'to', 'my', 'can', 'you', 'when', 'will', 'of', 'for', 'me',
              'in', 'on', 'it', 'we', 'get', 'does'}

# A FAQ counts as a match only if at least half of its keywords
# appear in what the user typed. This stops weak, accidental matches.
MIN_SCORE = 0.5


def load_faq_data(filename):
    """Open the JSON file and return its data (None if something is wrong)."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Please ensure it's in the same folder.")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' is not valid JSON.")
    return None


def get_words(text):
    """Turn a sentence into a set of useful lowercase words.
    Example: 'What are your HOURS?' -> {'hours'}"""
    # \b\w+\b picks out whole words and ignores punctuation like ? or !
    all_words = set(re.findall(r'\b\w+\b', text.lower()))
    return all_words - STOP_WORDS   # remove the filler words


def get_matching_answers(user_input, faqs):
    """Return the answers of ALL FAQs that match the user's message,
    best match first. Empty list = we are not confident about anything."""
    user_words = get_words(user_input)
    matches = []

    for faq in faqs:
        faq_words = get_words(faq['question'])
        if not faq_words:          # skip questions made only of filler words
            continue

        # Score = fraction of the FAQ's keywords found in the user's message
        # e.g. FAQ keywords {hours, operation}, user said "hours" -> 1/2 = 0.5
        score = len(user_words & faq_words) / len(faq_words)

        if score >= MIN_SCORE:
            matches.append((score, faq['answer']))

    matches.sort(reverse=True)                  # highest score first
    return [answer for score, answer in matches]  # keep only the answers


def is_greeting(user_input, greetings):
    """True if the message contains a greeting as a WHOLE word or phrase.
    Whole-word matching stops 'hi' from matching inside 'internship'."""
    for g in greetings:
        # \b = word boundary, re.escape = treat g as plain text
        if re.search(rf'\b{re.escape(g)}\b', user_input):
            return True
    return False


def run_chatbot():
    """Main loop. The bot moves through states: greeting -> chatting -> exit."""
    data = load_faq_data('sample_faq.json')
    if not data:
        return                      # stop if the data could not be loaded

    greetings = data.get('greetings', [])
    faqs = data.get('faqs', [])

    print("=============================================")
    print("   Welcome to the Customer Support Bot!      ")
    print("   Type 'bye', 'exit', or 'quit' to leave.   ")
    print("=============================================")

    state = "greeting"              # the conversation starts here

    while state != "exit":
        try:
            # Normalize: strip spaces and make lowercase
            user_input = input("\nYou: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            user_input = "bye"      # Ctrl+C / Ctrl+D leave politely

        if not user_input:          # user just pressed Enter
            continue

        # Step 1: exit check. We look at each word, so "ok bye!" also works.
        if set(re.findall(r'\w+', user_input)) & EXIT_WORDS:
            print("Bot: Goodbye! Have a great day.")
            state = "exit"
            continue

        # Step 2: try the FAQs first, so "hi, what are your hours?"
        # gets a real answer instead of only a hello.
        answers = get_matching_answers(user_input, faqs)
        if answers:
            for answer in answers:  # more than one = multi-intent question
                print(f"Bot: {answer}")
            state = "chatting"

        # Step 3: a plain greeting
        elif is_greeting(user_input, greetings):
            print("Bot: Hello there! How can I assist you today?")
            state = "chatting"

        # Step 4: fallback when we don't understand
        else:
            print("Bot: I'm sorry, I didn't quite understand that. Could you rephrase?")
            print("     (Hint: Try asking about 'hours', 'submit project', or 'certificate')")


if __name__ == "__main__":
    run_chatbot()