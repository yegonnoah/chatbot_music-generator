import json
from difflib import get_close_matches
from typing import Optional


def load_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, question: list[str]) -> Optional[str]:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, base: dict) -> Optional[str]:
    for q in base["question"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    base: dict = load_base('base.json')

    while True:
        user_input: str = input('you: ')

        if user_input.lower() == 'quit':
            break

        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in base["question"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t the answer, could you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                base["question"].append({"question": user_input, "answer": new_answer})
                save_base('base.json', base)
                print('Bot: Thank you! I learned a new response!')


if __name__ == '__main__':
    chat_bot()
