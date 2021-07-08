from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def start():
    """ Create homepage with start button. """

    session["responses"] = []
    # can derive question_id from responses
    session["question_id"] = 0

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

    if question_id != session["question_id"]:
        flash("We brought you back to your current question")
        return redirect (f"/questions/{session['question_id']}")
    elif session["question_id"] == len(survey.questions):
        return redirect ("/completion")
    else: 
        return render_template("question.html",
                            question=survey.questions[question_id],
                            question_id=question_id)


@app.route("/answer", methods=["POST"])
def answer_page():
    """ Appends answer to session and redirects to next question
        if next question outside of range of questions, redirect
        to completion page.
    """
# session["responses"].append.....
    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses

    session["question_id"] += 1

    if session["question_id"] < len(survey.questions):
        return redirect(f"/questions/{session['question_id']}")
    else:
        return redirect("/completion")


@app.route("/completion")
def completed_survey():
    """ Provides confirmation of survey completion. """

    return render_template("completion.html")
