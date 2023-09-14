from PIL import Image, ImageDraw, ImageFont
from flask import redirect, render_template, session
from functools import wraps
import sqlite3


def apology(message, code=400):
    """Render message as an apology to user."""
    img = Image.open("./static/gato_de_botas.jpg")
    draw = ImageDraw.Draw(img)
    fonte = ImageFont.truetype("./static/emmasophia.ttf", 20)
    draw.text((25, 25), message, font=fonte)
    draw.text((25, 500), str(code), font=fonte)
    img.save("./static/gato_escrito.png")

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
    # Configurações do envelope e da fonte
    ph = '"' + phrase + '"' + f" -{author}"
    envelope_image_path = "./static/envelope_aberto.png"
    output_image_path = "./static/envelope_escrito.png"
    x_left = 20
    x_right = 314
    y = 25
    line_height = 20

    # Abre a imagem do envelope
    img = Image.open(envelope_image_path)
    draw = ImageDraw.Draw(img)

    # Fonte inicial
    font_size = 18
    font_path = "./static/SundayPizza.ttf"
    font = ImageFont.truetype(font_path, font_size)

    # Separa a frase em palavras
    words = ph.split(" ")

    # Texto parcial
    phrase_partial = ""

    # # Função para calcular a largura do texto em pixels
    def text_width(text, font):
        return draw.textsize(text, font=font)[0]

    for word in words:
        phrase_partial += " " + word
        if y > 150:
            x_left = 35
            x_right = 290
        if text_width(phrase_partial, font) > x_right:
            tamanho = len(word) + 1
            phrase_partial = phrase_partial[:-tamanho]
            draw.text((x_left, y), phrase_partial, (0, 0, 0), font=font)
            y += line_height
            phrase_partial = word
    
    largura_do_espaco = 5
    tamanho_phrase = text_width(phrase_partial, font)
    espaco_sobrando = 335 - int(tamanho_phrase)
    quant_espaco = int(espaco_sobrando / (largura_do_espaco * 2)) - 2
    phrase_partial = " " * quant_espaco + phrase_partial

    draw.text((x_left, y), phrase_partial, (0, 0, 0), font=font)
    # Salva a imagem
    img.save(output_image_path)


def search_db(query, *args):
    con = sqlite3.connect("history.db")
    db = con.cursor()

    if query.split(" ")[0] == "SELECT":
        db.execute(query, args)
        columns = [desc[0] for desc in db.description]
        items = db.fetchall()
        info = [dict(zip(columns, list(item))) for item in items]
        con.close()
        return info
    else:
        db.execute(query, args)
        con.commit()
        con.close()
        return
