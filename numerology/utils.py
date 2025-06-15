from datetime import date
from collections import Counter
import random
import unicodedata
import re
import os

# ==== Normalize name ====
def normalize_name(name: str) -> str:
    name = unicodedata.normalize('NFD', name)
    name = ''.join(ch for ch in name if unicodedata.category(ch) != 'Mn')
    name = re.sub(r'[^A-Za-z ]', '', name)
    return name

# ==== Get vowels (universal) ====
def get_vowels() -> set:
    return set('AEIOU')  # language-independent base set

# ==== Numerology Core Tools ====

def reduce_single_digit(n, karmic_log=None):
    if karmic_log is None:
        karmic_log = set()
    while n > 9:
        if n in {13, 14, 16, 19}:
            karmic_log.add(n)
        n = sum(int(d) for d in str(n))
    return n


def reduce_digits(n, karmic_log=None):
    if karmic_log is None:
        karmic_log = set()
    while n not in {11, 22} and n > 9:
        if n in {13, 14, 16, 19}:
            karmic_log.add(n)
        n = sum(int(d) for d in str(n))
    return n

def letter_value_map():
    # Mapping theo hệ thống Pythagorean trong ảnh đính kèm
    return {
        'A': 1, 'J': 1, 'S': 1,
        'B': 2, 'K': 2, 'T': 2,
        'C': 3, 'L': 3, 'U': 3,
        'D': 4, 'M': 4, 'V': 4,
        'E': 5, 'N': 5, 'W': 5,
        'F': 6, 'O': 6, 'X': 6,
        'G': 7, 'P': 7, 'Y': 7,
        'H': 8, 'Q': 8, 'Z': 8,
        'I': 9, 'R': 9
    }

# ==== Numerology Calculations ====
def calculate_life_path(birthdate: date, karmic_log=None):
    digits = [int(d) for d in birthdate.strftime('%Y%m%d')]
    total = sum(digits)
    while total not in {10,11,22} and total > 9:
      if total in {13, 14, 16, 19}:
            karmic_log.add(total)
      total = sum(int(d) for d in str(total))
    return total

def calculate_expression_number(firstname: str, lastname: str, karmic_log=None) -> int:
    values = letter_value_map()
    full_name = f"{firstname} {lastname}".strip()
    name = normalize_name(full_name)
    return reduce_digits(sum(values.get(ch.upper(), 0) for ch in name if ch.isalpha()), karmic_log)

def calculate_soul_urge_number(firstname: str, lastname: str, karmic_log=None) -> int:
    vowels = get_vowels()
    values = letter_value_map()
    full_name = f"{firstname} {lastname}".strip()
    name = normalize_name(full_name)
    total = 0
    name_upper = name.upper()
    for i, ch in enumerate(name_upper):
        if ch == 'Y':
            prev = name_upper[i - 1] if i > 0 else ''
            next = name_upper[i + 1] if i + 1 < len(name_upper) else ''
            if (prev in vowels) or (next in vowels):
                continue  # Y is a consonant
            else:
                total += values.get('Y', 0)
        elif ch in vowels:
            total += values.get(ch, 0)
    return reduce_digits(total, karmic_log)


def calculate_personality_number(firstname: str, lastname: str, karmic_log=None) -> int:
    vowels = get_vowels()
    values = letter_value_map()
    full_name = f"{firstname} {lastname}".strip()
    name = normalize_name(full_name)
    total = 0
    name_upper = name.upper()
    for i, ch in enumerate(name_upper):
        if ch == 'Y':
            prev = name_upper[i - 1] if i > 0 else ''
            next = name_upper[i + 1] if i + 1 < len(name_upper) else ''
            if (prev in vowels) or (next in vowels):
                total += values.get('Y', 0)  # Y is a consonant
        elif ch.isalpha() and ch not in vowels:
            total += values.get(ch, 0)
    return reduce_digits(total, karmic_log)

def calculate_attitude_number(birthdate: date, karmic_log=None) -> int:
    return reduce_single_digit(birthdate.day + birthdate.month, karmic_log)

def calculate_natural_ability_number(birthdate: date, karmic_log=None) -> int:
    return reduce_digits(birthdate.day, karmic_log)

def calculate_thinking_capacity_number(firstname: str) -> int:
    name = normalize_name(firstname)
    values = letter_value_map()
    return reduce_single_digit(sum(values.get(ch.upper(), 0) for ch in name if ch.isalpha()))


# def calculate_maturity_number(life_path: int, expression: int) -> int:
#    return reduce_digits(life_path + expression)

def calculate_karmic_numbers(firstname, lastname, birthdate):
    karmic_log = set()
    calculate_life_path(birthdate, karmic_log)
    calculate_expression_number(firstname, lastname, karmic_log)
    calculate_soul_urge_number(firstname, lastname, karmic_log)
    calculate_personality_number(firstname, lastname, karmic_log)
    calculate_natural_ability_number(birthdate, karmic_log)
    reduce_single_digit(birthdate.day + birthdate.month, karmic_log)
    return sorted(karmic_log)

# def calculate_birthday_chart(birthdate: date) -> dict:
#     digits = [int(d) for d in birthdate.strftime('%d%m%Y')]
#     return dict(Counter(digits))

# def calculate_personal_years(birthdate: date, start_year: int = None, count: int = 3) -> dict:
#     if not start_year:
#         from datetime import datetime
#         start_year = datetime.now().year
#     results = {}
#     for i in range(count):
#         year = start_year + i
#         total = year + birthdate.day + birthdate.month
#         number = reduce_single_digit(total)
#         results[str(year)] = number
#     return results

# def calculate_pyramid_chart(birthdate: date) -> dict:
#     from datetime import datetime

#     # Rút gọn các thành phần ngày tháng năm
#     day = reduce_digits(birthdate.day)
#     month = reduce_digits(birthdate.month)
#     year = reduce_digits(birthdate.year)

#     # Tính các đỉnh
#     peak1 = reduce_digits(day + month)
#     peak2 = reduce_digits(day + year)
#     peak3 = reduce_digits(peak1 + peak2)
#     peak4 = reduce_digits(month + year)

#     # Tính năm dựa theo life path
#     life_path = calculate_life_path(birthdate)
#     birth_year = birthdate.year
#     peak_ages = {
#         2: [34, 43, 52, 61],
#         3: [33, 42, 51, 60],
#         4: [32, 41, 50, 59],
#         5: [31, 40, 49, 58],
#         6: [30, 39, 48, 57],
#         7: [29, 38, 47, 56],
#         8: [28, 37, 46, 55],
#         9: [27, 36, 45, 54],
#         10: [26, 35, 44, 53],
#         11: [25, 34, 43, 52],
#         22: [32, 41, 50, 59],
#     }
#     ages = peak_ages.get(life_path, [])
#     peak_years = [birth_year + age for age in ages]

#     return {
#         str(peak_years[0]): peak1,
#         str(peak_years[1]): peak2,
#         str(peak_years[2]): peak3,
#         str(peak_years[3]): peak4,
#     }

# ==== Meaning Fetcher ====
from .models import NumerologyMeaning

def get_meaning(type_code: str, number: str, language: str) -> str:
    meaning = NumerologyMeaning.objects.filter(
        type=type_code,
        number=number,
        language=language
    ).order_by('?').first()
    return meaning.content if meaning else "Meaning not found."

# ==== Azure OpenAI ====

from openai import AzureOpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
model_name = os.environ["AZURE_OPENAI_MODEL"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

# Tạo client AzureOpenAI
client = AzureOpenAI(
    api_key=subscription_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

LANGUAGE_NAMES = {
    "en": "English",
    "fi": "Finnish",
}
# Hàm gọi API sinh nội dung intro
def generate_azure_intro(fullname: str, birthdate: str, language: str,life_path_number: int) -> str:
    lang_name = LANGUAGE_NAMES.get(language, "English")  # fallback nếu không khớp
    prompt = (
        f"You are a gifted and soulful numerologist. Write a 2–3 sentence inspiring and poetic "
        f"numerology introduction for {fullname}, born on {birthdate}, in {lang_name}. "
        f"The Life Path Number is {life_path_number}. "
        f"Use rich emotional language and make each version feel unique.")
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content":     "You are a numerology assistant. Follow these rules strictly:\n"
                 "- The Life Path Number is already provided. Do NOT calculate or guess it.\n"
                 "- Always follow this structure: [Tone] + [Insight based on Life Path Number] + [Uplifting phrase].\n"
                 "- Do not mention exact calculation steps.\n"
                 "- Use a warm, supportive tone.\n"
                 "- If the language is Finnish, keep the grammar formal and clear."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=100,
            temperature=0.9,  # Tăng lên để có kết quả sáng tạo hơn
            top_p=0.95        # Kết hợp với temperature để đa dạng hóa output               
        )
        intro = response.choices[0].message.content
        return {
            "intro": intro,
            "prompt": prompt,
            "response": intro,
            "tokens_used": response.usage.total_tokens if hasattr(response, "usage") else 0,
            "model": response.model if hasattr(response, "model") else deployment
        }    
    except Exception as e:
        return {
            "intro": f"[AI error] {str(e)}",
            "prompt": prompt,
            "response": str(e),
            "tokens_used": 0,
            "model": deployment
        }

# ==== ID Generator ====
from .models import NumerologyResult

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode_base62(num):
    if num == 0:
        return BASE62_ALPHABET[0]
    base62 = ""
    while num > 0:
        num, rem = divmod(num, 62)
        base62 = BASE62_ALPHABET[rem] + base62
    return base62

def generate_unique_public_id():
    from django.utils.timezone import now
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status
    from .serializers import NumerologyRequestSerializer
    from datetime import date

    base_num = int(now().timestamp() * 1000)  # milliseconds for better uniqueness
    encoded = encode_base62(base_num + 12345)  # optional salt
    return encoded.rjust(9, '0')[:9]
