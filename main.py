from flask import Flask, request, render_template
import json
from difflib import get_close_matches

app = Flask(__name__)


def load_knowledge_base(file_path: str) -> dict:
 with open(file_path, 'r') as file:
    data: dict = json.load(file)
 return data


def save_knowlege_base(file_path: str, data: dict):
 with open(file_path, 'w') as file:
    json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
 matches: list = get_close_matches(
      user_question, questions, n=1,
      cutoff=0.8) #cutoff is how accurate the info is.
 return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
 for q in knowledge_base["questions"]:
    if q["question"] == question:
      return q["answer"]


def chat_bot():
 knowledge_base: dict = load_knowledge_base('knowledge_base.json')

 while True:
    user_input: str = request.form['user_input']

    if user_input.lower() == 'quit':
      break

    best_match: str | None = find_best_match(
        user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
      answer: str = get_answer_for_question(best_match, knowledge_base)
      return render_template('index.html', user_input=user_input, bot_response=answer)
    else:
      return render_template('index.html', user_input=user_input, bot_response='Sorry, I do not know the answer to that.')


@app.route('/', methods=['GET', 'POST'])
def index():
 if request.method == 'POST':
    return chat_bot()
 return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)