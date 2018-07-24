from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, ForeignKey, desc, func



class Drift(Base):
    """
        模型关联的特征在于，数据是实时的。
        数据的冗余，是一种历史状态的记录。
        对于具有记录状态的字段，最好不要做模型关联。
        合理利用冗余。
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))


    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        '''
        将数字类型，转为枚举类型
        '''
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        '''
        将枚举类型，转为数字类型
        '''
        self._pending = status.value

    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')



