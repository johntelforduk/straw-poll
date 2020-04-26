from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators, FieldList
from wtforms.fields.html5 import DecimalRangeField
from sys import argv
from dotenv import load_dotenv
from os import getenv
from users_table import UsersTable
import json


DEBUG_ENABLED = '-d' in argv


def debug(msg):
    """If in debug mode, send a debug message to stdout."""
    if DEBUG_ENABLED:
        print("Debug: {}".format(msg))


# Load POLL dictionary from JSON file.
f = open('poll.json', 'r')
whole_json = (f.read())
POLL = json.loads(whole_json)
f.close()
print(POLL)


print(json.dumps(POLL))


NUM_QUESTIONS = len(POLL)


app = Flask(__name__)
app.config['DEBUG'] = DEBUG_ENABLED


class PollForm(Form):
    """Make a new PollForm class, based on the Form class.
    Add some extra attributes compared to parent class."""

    # Email address of the user who voted in the poll. Used to make key in votes table.
    email = StringField(label='Your Email Address or Nickname', validators=[validators.Length(min=4, max=100)])

    # The sliders which will be used to get opinions from users.
    sliders = FieldList(DecimalRangeField(), min_entries=NUM_QUESTIONS, max_entries=NUM_QUESTIONS)

    label = []                          # Labels above each question.
    option1, option2 = [], []           # The options on either side of the sliders.
    option1_img, option2_img = [], []   # Images for options.

    def set_questions(self, parm_questions: list):
        # print(url_for('static', filename='Elon_Musk_2015.jpg'))

        for each_question in parm_questions:
            self.label.append(each_question['label'])
            self.option1.append(each_question['option1'])
            self.option2.append(each_question['option2'])

            # Work out the complete URL for each image file.
            self.option1_img.append(url_for('static', filename=each_question['option1_img']))
            self.option2_img.append(url_for('static', filename=each_question['option2_img']))


def calc_votes(all_votes: list) -> dict:
    """For parm list of list of votes, return a dictionary of average votes."""
    calc_results = {}            # Key=question_id, value=average score

    # Fill it with zeros.
    for each_question in POLL:
        calc_results[each_question['question_id']] = 0.0
    # print(results)

    # Add each users' votes to the results.
    num_users = 0
    for each_user in all_votes:
        num_users += 1
        for each_question in each_user:
            # print(each_question)
            calc_results[each_question['question_id']] += each_question['vote']

    # Work out the mean average.
    for each_question in calc_results:
        calc_results[each_question] = int(calc_results[each_question] / num_users)

    return calc_results


load_dotenv(verbose=True)           # Set operating system environment variables based on contents of .env file.

votes_table = UsersTable(table_name=getenv('VOTES_TABLE'))



@app.route("/", methods=['GET', 'POST'])
def home():
    form = PollForm()
    form.set_questions(parm_questions=POLL)


    if request.method == 'GET':
        return render_template('poll_form.html', parm_form=form)

    # Method must be 'POST'.
    else:
        # Make a votes dictionary that represents the user's votes.
        votes = []
        pos = 0
        for each_item in request.form:
            debug('each_item={}  request.form[each_item]={}'.format(each_item, request.form[each_item]))
            if 'sliders' in each_item:
                question_id = POLL[pos]['question_id']
                vote = float(request.form[each_item])

                this_vote = {'question_id': question_id,
                             'vote': vote}
                votes.append(this_vote)
                pos += 1

        if DEBUG_ENABLED:
            print('debug: votes=', votes)

        # Get email address from form.
        email = request.form['email']

        # Store their votes in DynamoDB.
        votes_table.put(user_id=email, value=votes)

        return redirect(url_for('results'))


@app.route("/results", methods=['GET'])
def results():

    votes = votes_table.scan_values()
    scores = calc_votes(votes)

    # print('scores=', scores)

    # Make list of dictionaries with everything in them needed for results page.
    results_list = []
    for each_question in POLL:
        this_question_id = each_question['question_id']
        question_plus_vote = each_question
        question_plus_vote['vote'] = scores[this_question_id]
        results_list.append(question_plus_vote)

    print(results_list)

    # Render template for results, passing list to it as parm.
    return render_template('results.html',
                           parm_results_list=results_list)


if __name__ == "__main__":
    app.run()
