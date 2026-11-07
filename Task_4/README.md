# Rule-Based Interactive Terminal Assistant/Chatbot

A simple command-line chatbot that answers FAQs using keyword matching and regular expressions. No machine learning and no external libraries, just Python 3's built-in `re` and `json` modules.

## Features

- Loads greetings and FAQs from a JSON file, so you can add questions without touching the code
- Cleans user input (lowercase, strips spaces and punctuation, ignores filler words)
- Multi-intent matching: one message can get several answers
- Fallback reply when the bot isn't confident about the question
- Clean exit with `bye`, `exit` or `quit` (also works inside a sentence like "ok bye!")
- Error handling for a missing or broken JSON file, empty input, and Ctrl+C / Ctrl+D

## Requirements

- Python 3.6 or newer (no `pip install` needed)

## Project Structure

```
.
├── chatbot.py   # the chatbot
├── sample_faq.json     # greetings and FAQ data
└── README.md
```

## How to Run

Keep `chatbot.py` and `sample_faq.json` in the same folder, then run:

```bash
python chatbot.py
```

## Example Conversation

```
You: hello
Bot: Hello there! How can I assist you today?

You: How do I submit my internship project?
Bot: You can submit your public GitHub repository link through your Student Workspace.

You: what are your hours and when will i get my certificate
Bot: We operate Monday through Friday from 9:00 AM to 6:00 PM IST.
Bot: Certificates are reviewed and issued within 3-5 business days after your code review.

You: what is the weather
Bot: I'm sorry, I didn't quite understand that. Could you rephrase?
     (Hint: Try asking about 'hours', 'submit project', or 'certificate')

You: ok bye!
Bot: Goodbye! Have a great day.
```

## How It Works

1. **Load:** the greetings and FAQs are read from `sample_faq.json`.
2. **Normalize:** the input is lowercased, and a regex (`\b\w+\b`) extracts the words. Filler words such as "what", "the" and "your" are removed.
3. **Score:** for every FAQ, the bot calculates the share of that question's keywords found in the user's message.
4. **Answer:** every FAQ scoring at least `0.5` is answered, best match first. This is what allows multi-intent questions.
5. **Fallback:** if nothing scores high enough, the bot asks the user to rephrase and suggests topics.

### Conversation states

```
greeting  ->  chatting  ->  exit
```

The bot starts in `greeting`, moves to `chatting` after any greeting or answered question, and ends in `exit` when the user says bye, exit or quit.

### Order of checks for each message

1. Exit words
2. FAQ match (so "hi, what are your hours?" gets a real answer, not just a hello)
3. Plain greeting
4. Fallback

## Adding or Changing FAQs

Edit `sample_faq.json`. No code changes are needed.

```json
{
  "greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
  "faqs": [
    {
      "question": "What are your hours of operation?",
      "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
    }
  ]
}
```

Tips for writing questions:
- Use clear keywords, because matching is based on the meaningful words in the question.
- If users say a topic in different ways (for example "timings" for "hours"), add the extra word to the question text or to `STOP_WORDS` / matching logic in the code.

## Configuration

Two constants at the top of `chatbot.py` control the matching:

| Constant | Purpose | Default |
|---|---|---|
| `MIN_SCORE` | Share of a FAQ's keywords that must appear in the input. Raise it for stricter matching, lower it for looser matching. | `0.5` |
| `STOP_WORDS` | Filler words ignored during matching. | see file |

## Limitations

- Matching is keyword-based, so it does not understand meaning, spelling mistakes or synonyms that are not in the FAQ question.
- Very short questions with one keyword can match more than one FAQ if they share that word.
- Only English is supported.

## Testing Checklist

| Input | Expected result |
|---|---|
| `hello` | Greeting reply |
| `How do I submit my internship project?` | Submit answer only (no false greeting) |
| `hours and certificate` | Both answers |
| `when is the deadline` | Fallback |
| *(blank Enter)* | Ignored |
| `ok bye!` | Goodbye and exit |
| Missing or invalid `sample_faq.json` | Friendly error message |