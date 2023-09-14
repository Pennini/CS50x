from PIL import Image, ImageDraw, ImageFont
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    img = Image.open('./static/gato_de_botas.jpg')
    draw = ImageDraw.Draw(img)
    fonte = ImageFont.truetype('./static/emmasophia.ttf', 20)
    draw.text((25, 25), message, font=fonte)
    draw.text((25, 500), str(code), font=fonte)
    img.save('./static/gato_escrito.png')

    return render_template("apology.html", top=code), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def write_envelope(phrase, author):
    ph = '"'+ phrase + '" -' + author
    y = 35
    x = 22
    l = 40
    img = Image.open('./static/envelope_aberto.png')
    draw = ImageDraw.Draw(img)
    fonte = ImageFont.truetype('./static/SundayPizza.ttf', 18)
    letters = 0
    phrase_partial = ''
    words = ph.split(" ")
    for index, word in enumerate(words):
        letters += 1 + len(word)
        if y == 175:
            x = 55
            l = 35
        elif y == 195:
            x = 90
            l = 30
        if letters > l or index == len(words) - 1:
            phrase_partial += word + ' '
            draw.text((x, y), phrase_partial, (0, 0, 0), font=fonte)
            y += 20
            phrase_partial = ''
            letters = 0
            continue
        phrase_partial += word + ' '
    img.save('./static/envelope_escrito.png')