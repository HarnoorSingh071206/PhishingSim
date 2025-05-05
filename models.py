from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    submitted = db.Column(db.Boolean, default=False)

    submitted_username = db.Column(db.String(120))
    submitted_password = db.Column(db.String(120))


class Multiple(db.Model):
    __tablename__ = 'multiple'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent = db.Column(db.Boolean, default=False)

    # One-to-many relationship
    targets = db.relationship('Target', backref='multiple', lazy=True, cascade="all, delete-orphan")


class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    sent = db.Column(db.Boolean, default=False)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    submitted = db.Column(db.Boolean, default=False)

    submitted_username = db.Column(db.String(120))
    submitted_password = db.Column(db.String(120))

    multiple_id = db.Column(db.Integer, db.ForeignKey('multiple.id'), nullable=False)
