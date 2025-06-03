# Teaching Assistant Chatbot

This chatbot integrates with the Teaching Assistant analytics tool to provide natural language interaction with student data using OpenRouter LLM API.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get an API key from OpenRouter (https://openrouter.ai)

3. Set your API key as an environment variable:
   ```
   export OPENROUTER_API_KEY="your_api_key_here"
   ```
   
   Or pass it directly when running the script:
   ```
   python ta_chatbot.py --api-key "your_api_key_here"
   ```

## Usage

Run the chatbot:
```
python ta_chatbot.py
```

### Available Commands

- `student: [name]` - Focus on a specific student (e.g., `student: Johnson, Katrice`)
- `at-risk` - List students who are at risk based on completion percentage
- `module: [number]` - Get information about a specific module (1-6)
- `clear` - Clear the current student focus
- `help` - Show available commands
- `exit` or `quit` - End the conversation

### Example Questions

When no specific student is selected:
- "Who are the top 3 students in the class?"
- "Which module has the lowest average completion rate?"
- "How many students are behind on their labs?"
- "What percentage of students have completed all modules?"

When a student is selected:
- "What modules has this student completed?"
- "How is their study consistency?"
- "What recommendations do you have for this student?"
- "How does this student compare to the class average?"

## Customizing the Model

By default, the chatbot uses `openai/gpt-3.5-turbo`. You can specify a different model with the `--model` flag:

```
python ta_chatbot.py --model "anthropic/claude-3-opus-20240229"
```

See OpenRouter documentation for available models.

## Integration with Teaching Assistant Tool

The chatbot leverages the existing Teaching Assistant analytics tool to access:
- Student progress data
- Module completion statistics
- At-risk student identification
- Personalized recommendations

This allows instructors to interact with the data in a more natural way through conversation rather than command-line flags.
