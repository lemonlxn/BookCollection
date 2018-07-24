from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookSingleModel
from app.view_models.drift import DriftCollection
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):

    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你的，不能向自己索要书籍哈')
        return redirect(url_for('web.book_detail',isbn = current_gift.isbn))

    # 判断当前用户能否发送鱼漂(鱼豆>=1，每索取两本书，必须送出一本书)
    can_send_drift = current_user.can_send_drift()

    if not can_send_drift:
        # 如果不能发送鱼漂，显示当前用户鱼豆
        return render_template('not_enough_beans.html',beans = current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form,current_gift)
        send_mail(current_gift.user.email,
                  '有人想要一本书',
                  'email/get_gift.html',
                  wisher = current_user,
                  gift = current_gift)
        return redirect(url_for('web.pending'))

    # 获取赠送者信息
    gifter = current_gift.user.summary
    return render_template('drift.html',
                           gifter = gifter,
                           user_beans = current_user.beans,
                           form = form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
                or_(Drift.requester_id == current_user.id
                    ,Drift.gifter_id == current_user.id)).\
        order_by(desc(Drift.create_time)).all()
    view = DriftCollection(drifts,current_user.id)
    return render_template('pending.html',drifts=view.data)



@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id = current_user.id,
            id = did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1

        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        wish = Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False)
        wish.launched = True
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()

        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookSingleModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        # 向其他用户请求书籍，本身消耗一个鱼豆
        try:
            if current_user.beans>=1:
                current_user.beans -= 1
        except Exception as e:
            raise e

        db.session.add(drift)



