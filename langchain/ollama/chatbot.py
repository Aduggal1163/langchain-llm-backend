import ollama
conversation=[
    {
        'role':'system',
        'content':"You are a helpful AI assistant. Give clear and concise answers."
    }
]
max_history = 6
print("Type 'exit' to quit \n")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    #add user message to history
    conversation.append({
        'role' : 'user',
        'content' : user_input
    })
    # history trimming
    # If you dont limit history:
    # Context keeps growing
    # Model slows down
    # Memory increases
    # Token cost increases (in real systems)

    system_message = conversation[0]
    other_message = conversation[1:]
    if(len(other_message) > max_history) : 
        other_message = other_message[-max_history:]
    conversation = [system_message] + other_message

# You: My name is Abhishek
# You: I live in India
# You: I like Cricket
# You: I am learning AI
# You: I love Python
# You: I use Ollama
# You: What is my name?
# trimming works:
# The first message (“My name is Abhishek”) may disappear
# → Model might NOT remember your name.

    # Print convo length
    print(f"current convo length is : {len(conversation)}")
    #send full conversation to model
    response = ollama.chat(
        model = 'llama3.2:1b',
        messages=conversation
    )
    assistant_reply = response['message']['content']
    #add assistant reply to history
    conversation.append({
        'role' : 'assistant',
        'content' : assistant_reply
    })
    print("Bot: ", assistant_reply)
