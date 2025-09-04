
from transformers import pipeline

# Load FLAN-T5 (large gives more creative responses than base)
generator = pipeline("text2text-generation", model="google/flan-t5-large")

print("Type 'exit' to quit.\n")

while True:
    user_prompt = input("Enter your prompt: ")
    if user_prompt.lower() == "exit":
        break

    # Generate response (poem-friendly setup)
    output = generator(
        user_prompt,
        max_new_tokens=150,        # enough for a small poem
        num_beams=5,               # beam search = more coherent
        no_repeat_ngram_size=3,    # avoids repetition
        early_stopping=True
    )

    print("\nGenerated Response:\n")
    print(output[0]['generated_text'])
    print("\n" + "-"*60 + "\n")
