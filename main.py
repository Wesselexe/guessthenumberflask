from flask import Flask, render_template, request, make_response, redirect, url_for
from models import Player
from random import randint

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    email = request.cookies.get('email')

    if email:
        user = Player.fetch_one(query=['email', '==', email])
    else:
        user = None

    return render_template('index.html', user=user)


@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    email = request.form.get('email')

    user = Player.fetch_one(query=['email', '==', email])
    secret_number = randint(1, 30)

    if not user:
        user = Player(name=name, email=email, secret_number=secret_number)
        user.create()

    response = make_response(redirect(url_for('index')))
    response.set_cookie('email', email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    email = request.cookies.get("email")

    user = Player.fetch_one(query=['email', '==', email])

    if guess == user.secret_number:
        message = "Correct! The secret number is {0}".format(str(guess))
        Player.edit(obj_id=Player.id, secret_number=Player.make_secret_number())

    elif guess > user.secret_number:
        message = "Your guess is not correct... try something smaller."

    elif guess < user.secret_number:
        message = "Your guess is not correct... try something bigger."

    return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()
