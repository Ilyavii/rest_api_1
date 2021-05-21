from app import db, session, Base


class User(Base):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(500), nullable=False)
    mail = db.Column(db.String(500), nullable=False)
    transaction = db.Column(db.String(500), nullable=False)
    data = db.Column(db.String(500), nullable=False)
