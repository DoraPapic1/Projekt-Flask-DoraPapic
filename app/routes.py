from flask import Blueprint, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from .models import Income, Expense, SavingGoal
from . import db
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Dohvaćanje svih prihoda i rashoda
    incomes = Income.query.all()
    expenses = Expense.query.all()

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    balance = total_income - total_expense

    return render_template('home.html', incomes=incomes, expenses=expenses, balance=balance)

@main.route('/add-income', methods=['GET', 'POST'])
def add_income():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']

        new_income = Income(amount=amount, description=description)
        db.session.add(new_income)
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('add_income.html')

@main.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']

        new_expense = Expense(amount=amount, description=description)
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('add_expense.html')
@main.route('/delete-income/<int:income_id>', methods=['POST'])
def delete_income(income_id):
    # Dohvati prihod po ID-u i izbriši ga
    income = Income.query.get_or_404(income_id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/delete-expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    # Dohvati rashod po ID-u i izbriši ga
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/goals', methods=['GET', 'POST'])
def goals():
    if request.method == 'POST':
        name = request.form['name']
        target_amount = float(request.form['target_amount'])
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')

        new_goal = SavingGoal(name=name, target_amount=target_amount, deadline=deadline)
        db.session.add(new_goal)
        db.session.commit()

        return redirect(url_for('main.goals'))

    goals = SavingGoal.query.all()
    return render_template('goals.html', goals=goals)

@main.route('/add-to-goal/<int:goal_id>', methods=['POST'])
def add_to_goal(goal_id):
    goal = SavingGoal.query.get_or_404(goal_id)
    amount = float(request.form['amount'])

    goal.current_amount += amount
    db.session.commit()

    return redirect(url_for('main.goals'))

@main.route('/delete-goal/<int:goal_id>', methods=['POST'])
def delete_goal(goal_id):
    goal = SavingGoal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return redirect(url_for('main.goals'))

@main.route('/graphs')
def graphs():
    incomes = Income.query.all()
    expenses = Expense.query.all()

    # Priprema podataka
    income_data = [income.amount for income in incomes]
    expense_data = [expense.amount for expense in expenses]
    labels = ['Prihodi', 'Rashodi']
    values = [sum(income_data), sum(expense_data)]

    # Generiranje pie chart-a
    img = io.BytesIO()
    plt.figure(figsize=(6, 6))
    colors = ['#A2D5C6', '#BC6C25']
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Raspodjela prihoda i rashoda')
    plt.savefig(img, format='png')
    img.seek(0)
    pie_chart = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    # Generiranje bar chart-a
    img = io.BytesIO()
    plt.figure(figsize=(8, 5))
    bars = ['Prihodi', 'Rashodi']
    values = [sum(income_data), sum(expense_data)]
    bar_colors = ['#A2D5C6', '#BC6C25']
    plt.bar(bars, values, color=bar_colors)
    plt.title('Ukupni prihodi i rashodi')
    plt.xlabel('Kategorije')
    plt.ylabel('Iznos (EUR)')
    plt.savefig(img, format='png')
    img.seek(0)
    bar_chart = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return render_template('graphs.html', pie_chart=pie_chart, bar_chart=bar_chart)  