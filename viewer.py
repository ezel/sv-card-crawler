from flask import Flask, render_template, request
from model import Card
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello index'

@app.route('/test')
def test():
    return 'Test here'

@app.route('/card')
@app.route('/card/<cid>')
def card(cid=0):
    cards = [c for c in Card.select().where(Card.cid == cid) ]
    if len(cards) > 0:
        return render_template('card.html', cards=cards)
    else:
        return 'no card find with %s' % cid

@app.route('/sql')
def sql():
    pass
