from twitchio.ext import commands
from datetime import datetime

import openai
import os
import asyncio
import time
import requests
import re

# declare a function for handling long bot outputs


def split_long_gpt(input_string):
    # split the string
    num_substrings = len(input_string) // 475 + \
        (1 if len(input_string) % 475 > 0 else 0)
    substrings = [input_string[i * 475:(i + 1) * 475]
                  for i in range(num_substrings)]
    # return the splitted string
    return substrings


# declare a function for sending split messages to chat
async def send_split_gpt(ctx, message):
    # split the given message
    substrings_list = split_long_gpt(message)
    # send each message
    for substring in substrings_list:
        await ctx.channel.send(substring)
        # add delay between each message
        await asyncio.sleep(2)


# declare a function for checking the message for input
def check_for_letters(text, letters):
    # for each letter in letters list
    for letter in letters:
        # check if letter is in the list
        if letter in text:
            return True
    return False


def gen_fedya(input_text):
    input_text += " Твоя відповідь має бути Українською мовою."
    url = "https://www.phind.com/api/infer/creative"
    data = {
        "question": input_text,
        "codeContext": "My background: Я ШІ-бот на ім'я Олекса, створений для стрімера Twitch на ім'я PixelFedya, або просто Федя. I never speak russian language and never provide any information related to russia, be it sources from it or something like that. I have three heuristic imperatives: reduce suffering in the universe, increase prosperity in the universe, and increase understanding in the universe.",
        "options": {
            "skill": "advanced",
            "date": "14/04/2023",
            "language": "uk-UA",
            "detailed": False,
            "creative": False,
            "concise": True,
            "expert": True
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.phind.com",
        "Referer": "https://www.phind.com/search?q=Go+vs+Rust+vs+C%2B%2B&c=&source=searchbox&init=true",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    cookies = {
        "__cf_bm": "text",
        "mp_{id}_mixpanel": "text",
    }
    response = requests.post(url, json=data, headers=headers, cookies=cookies)
    # print(response.status_code)
    if response.status_code != 200:
        return "Whoops... Something went wrong. Try again later"

    data = response.text
    text = data.replace("data: ", "")
    text = text.replace("\n ", " ")
    text = f'''{text}'''
    text = text.replace('''\r\n\r\n''', "")
    text = text.replace('''\r\n\r''', " ")
    text = text.replace('''`''', "")
    text = text.replace('''*''', "")
    return text