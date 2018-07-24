
from app.models.gift import Gift
from app.view_models.book import BookSingleModel
from flask import render_template
from . import web




@web.route('/')
def index():
    recent_gift = Gift.recent_gifts()
    book = [BookSingleModel(gift.book) for gift in recent_gift]
    return render_template('index.html',recent=book)


@web.route('/personal')
def personal_center():
    pass
