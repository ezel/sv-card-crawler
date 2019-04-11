from flask import Flask, render_template, request
from model import Card
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello index'

@app.route('/test')
def test():
    return 'Test here'

@app.route('/card/<cid>')
def card(cid):
    lang = request.args.get('lang') or 'en'
    card = Card.select().where(Card.cid == cid).where(Card.language == lang).first()
    if card:
        return render_template('card.html', card=card)
    else:
        return 'no %s card find with %s' % (lang, cid)

@app.route('/sql')
def sql():
    pass

@app.route('cards')
def cards():
    pass
