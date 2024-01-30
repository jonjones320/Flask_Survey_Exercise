from flask import Flask, render_template, redirect, request, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "password137"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
question_index = 0

@app.route('/')
def home_page():

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("home.html", title=title, instructions=instructions)

@app.route('/questions/<int:question_index>')
def question_page(question_index):

    if (0 <= question_index < len(satisfaction_survey.questions)) and not (question_index < len(responses)): 
        question = satisfaction_survey.questions[question_index].question
        choices = satisfaction_survey.questions[question_index].choices
        return render_template("questions.html", question=question, choices=choices, question_index=question_index)
    
    if len(satisfaction_survey.questions) == len(responses):
        return render_template("thankyou.html")
    
    if question_index != len(responses):
        flash("You have violated the integrity of this survey.")
        return render_template("thankyou.html")

    else:
        return render_template("thankyou.html")
    
@app.route('/answer/<int:question_index>', methods=['POST'])
def answer_page(question_index):

    answer = request.form.get('choice')
    responses.append(answer)

    return redirect(url_for('question_page', question_index=question_index+1))