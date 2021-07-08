from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def start():

    return render_template("survey_start.html",
                           survey_title=survey.title,
                           survey_instructions=survey.instructions)


@app.route("/begin", methods=["POST"])
def survey_begin():

    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def questions(question_id):

    return render_template("question.html",
                           question=survey.questions[question_id])


@app.route("/answer", methods=["POST"])
def answer_page():

    ans = request.form["answer"]
    responses.append(ans)

    return ans
