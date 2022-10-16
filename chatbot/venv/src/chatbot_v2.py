from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger(torch.__name__).setLevel(logging.ERROR)

model_name = "microsoft/DialoGPT-large"
# model_name = "microsoft/DialoGPT-medium"
# model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


for step in range(5):
    text = input(">>You: ")
    # encode the input and add end of string token
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    # concatenate new user input with chat history (if there is)
    bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=1) if step > 0 else input_ids
    # generate respone
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        do_sample=True,
        top_k=75,
        top_p=0.9,
        # num_return_sequences=5,
        temperature=0.6,
        pad_token_id=tokenizer.eos_token_id
    )

    # for one answer
    result = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print(f"Bot: {result}")

    # for multiple answers
    # for i in range(len(chat_history_ids)):
    #     output = tokenizer.decode(chat_history_ids[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
    #     print(f"DialoGPT {i}: {output}")
    # choice_index = int(input("Choose the response you want for the next input: "))
    # chat_history_ids = torch.unsqueeze(chat_history_ids[choice_index], dim=0)
