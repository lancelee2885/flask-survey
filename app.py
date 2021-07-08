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
    """ Create homepage with start button. """

    return render_template("survey_start.html",
                           survey_title=survey.title,
                           survey_instructions=survey.instructions)


@app.route("/begin", methods=["POST"])
def survey_begin():
    """ Redirects user to the first question of correct survey. """

    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def questions(question_id):
    """ Generates and returns question page from question_id. """

    return render_template("question.html",
                           question=survey.questions[question_id],
                           question_id=question_id)


@app.route("/answer", methods=["POST"])
def answer_page():
    """ Appends answer and redirects to next question
        if next question outside of range of questions, redirect
        to completion page.
    """

    responses.append(request.form["answer"])

    new_id = int(request.form["question-id"]) + 1

    if new_id < len(survey.questions):
        return redirect(f"/questions/{new_id}")
    else:
        return redirect("/completion")


@app.route("/completion")
def completed_survey():
    """ Provides confirmation of survey completion. """

    return render_template("completion.html")
