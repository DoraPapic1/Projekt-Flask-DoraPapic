from . import db

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

class SavingGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Naziv cilja
    target_amount = db.Column(db.Float, nullable=False)  # Ciljani iznos
    deadline = db.Column(db.Date, nullable=False)  # Rok
    current_amount = db.Column(db.Float, default=0.0)  # Trenutno ušteđeno
