from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_goals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FinancialGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, default=0)
    is_achieved = db.Column(db.Boolean, default=False)

def create_tables():
    db.create_all()

@app.route('/')
def index():
    goals = FinancialGoal.query.all()
    total_funded = sum(goal.current_amount for goal in goals)
    total_goals = sum(goal.total_amount for goal in goals)
    return render_template('index.html', goals=goals, total_funded=total_funded, total_goals=total_goals)

@app.route('/add', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        name = request.form.get('name')
        total_amount = request.form.get('total_amount', type=int)
        new_goal = FinancialGoal(name=name, total_amount=total_amount)
        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_goal.html')

@app.route('/edit/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = FinancialGoal.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal.name = request.form['name']
        goal.total_amount = request.form.get('total_amount', type=int)
        goal.current_amount = request.form.get('current_amount', type=int)
        goal.is_achieved = 'is_achieved' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_goal.html', goal=goal)

@app.route('/delete/<int:goal_id>')
def delete_goal(goal_id):
    goal = FinancialGoal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        create_tables()  # This now runs within the application context
    app.run(debug=True)
