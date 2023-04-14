import os
from random import randint
from random import shuffle
from flask import Flask, session, redirect, url_for, render_template, request
from db_scripts import get_question_after, check_answer, get_quizes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answer'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quiz_id = request.form.get('quiz')
        start_quiz(quiz_id)
        return redirect(url_for('test'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'quiz' not in session or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answer()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

@app.route('/result')
def result():
    html = render_template('result.html', right=session['answer'], total=session['total'])
    end_quiz()
    return html

def save_answer():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answer'] += 1

def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)

if __name__ == "__main__":
    app.run()