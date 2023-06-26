from twitchio.ext import commands
from datetime import datetime
import openai
import os
import asyncio
import queue
import time
import requests
import re
from vars import *
import g4f
from deep_translator import GoogleTranslator
from langdetect import detect
import random
from gpt4free import usesless
from notifypy import Notify


def split_long_gpt(input_string):
    num_substrings = len(input_string) // 440 + \
        (1 if len(input_string) % 440 > 0 else 0)
    substrings = [input_string[i * 440:(i + 1) * 440]
                  for i in range(num_substrings)]
    return substrings


async def send_split_gpt(ctx, message):
    substrings_list = split_long_gpt(message)
    for substring in substrings_list:
        await ctx.channel.send(substring)
        await asyncio.sleep(2)


def split_long_message(input_string):
    words = input_string.split()
    result = []
    for i in range(0, len(words), 10):
        result.append(" ".join(words[i:i+10]))
    return result


async def send_split_message(ctx, message):
    # split the given message
    substrings_list = split_long_message(message)
    # send each message
    for substring in substrings_list:
        await ctx.channel.send(substring)
        # add delay between each message
        await asyncio.sleep(6)


def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


def write_to_log(message, author, CHANNEL):
    # for handling current time
    now = datetime.now()
    # for handling the file name
    file_name = CHANNEL + "-log_" + now.strftime("%d-%m-%Y") + ".md"
    # for handling the file path
    file_path = os.path.join(log_dir, file_name)

    # open file with appropriate decoding
    with open(file_path, "a", encoding="utf-8") as log_file:
        # declare and output timestamp before message
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_file.write(timestamp)
        # output message with author name to log
        log_file.write(f"\n\n{author}: {message}\n")
        log_file.write(f"\n---\n\n")


#   <GENERATING MESSAGES>   #
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"


def openai_generate(input_text, context):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": input_text}
        ],
        max_tokens=280,
        temperature=0.7,
    )
    output_text = response['choices'][0]['message']['content']
    return output_text


def gpt4free_ua(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='uk').translate(input_text)
    response = g4f.ChatCompletion.create(
        model=g4f.Model.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": input_prompt
        }],
    )
    return clean_text(response)


def gpt4free_en(input_text):
    input_prompt = GoogleTranslator(
        source='auto', target='en').translate(input_text)
    response = g4f.ChatCompletion.create(
        model=g4f.Model.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": input_prompt
        }],
    )
    return clean_text(response)


global_messages = []


def gpt4free(input_text):
    global_messages.append(
        {
            "role": "user",
            "content": input_text
        }
    )
    response = g4f.ChatCompletion.create(
        model=g4f.Model.gpt_4,
        messages=global_messages,
    )
    global_messages.append(
        {
            "role": "model",
            "content": response
        }
    )
    return clean_text(response)


def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'\n', ' ', text)

    return text


def generate_ai_message(message):
    print("\nGenerating a message...\n")
    start_time = time.time()

    input_text = message.replace("piprly", "").replace(
        "wuyodo", "").replace("@", "")
    output_text = gpt4free(input_text)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nGenerated in {elapsed_time:.2f} seconds")
    return output_text
