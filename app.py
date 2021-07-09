from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from surveys import satisfaction_survey as survey
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():

    return render_template("index.html")


@app.route("/home", methods=["POST"])
def start():
    """ Create homepage with start button. """

    session["responses"] = []
    session["survey_type"] = request.form["survey-type"]

    return render_template("survey_start.html",
                           survey_title=surveys.surveys[session['survey_type']].title,
                           survey_instructions=surveys.surveys[session['survey_type']].instructions)


@app.route("/begin", methods=["POST"])
def survey_begin():
    """ Redirects user to the first question of correct survey. """

    return redirect(f"{session['survey_type']}/questions/0")


@app.route(f"{session['survey_type']}/questions/<int:question_id>")
def questions(question_id):
    """ Generates and returns question page from question_id. """

    if question_id != len(session["responses"]):
        flash("We brought you back to where you should be")
        return redirect(f"/questions/{len(session['responses'])}")
    elif len(session["responses"]) >= len(surveys.surveys[session['survey_type']].questions):
        return redirect("/completion")
    else:
        return render_template("question.html",
                               question=surveys.surveys[session['survey_type']].questions[question_id])


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

    if len(session["responses"]) < len(surveys.surveys[session['survey_type']].questions):
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        return redirect("/completion")


@app.route("/completion")
def completed_survey():
    """ Provides confirmation of survey completion. """

    return render_template("completion.html")
