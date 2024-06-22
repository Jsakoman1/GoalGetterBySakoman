from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_goals.db'  # SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your SQLAlchemy model
class FinancialGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, default=0)

# Function to create database tables
def create_tables():
    db.create_all()

# Route to display all goals and progress
@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'name')
    filter_by = request.args.get('filter_by', 'all')

    if filter_by == 'all':
        goals = FinancialGoal.query.order_by(sort_by).all()
    elif filter_by == 'completed':
        goals = FinancialGoal.query.filter(FinancialGoal.current_amount >= FinancialGoal.total_amount).order_by(sort_by).all()
    elif filter_by == 'in_progress':
        goals = FinancialGoal.query.filter(FinancialGoal.current_amount < FinancialGoal.total_amount).order_by(sort_by).all()

    total_funded = sum(goal.current_amount for goal in goals)
    total_goals = sum(goal.total_amount for goal in goals)

    for goal in goals:
        if goal.total_amount > 0:
            goal.progress = int((goal.current_amount / goal.total_amount) * 100)
        else:
            goal.progress = 0

    if total_goals > 0:
        total_progress = int((total_funded / total_goals) * 100)
    else:
        total_progress = 0

    return render_template('index.html', goals=goals, total_progress=total_progress, sort_by=sort_by, filter_by=filter_by)

# Route to add a new goal
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

# Route to edit an existing goal
@app.route('/edit/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = FinancialGoal.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal.name = request.form['name']
        goal.total_amount = request.form.get('total_amount', type=int)
        goal.current_amount = request.form.get('current_amount', type=int)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_goal.html', goal=goal)

# Route to delete a goal
@app.route('/delete/<int:goal_id>')
def delete_goal(goal_id):
    goal = FinancialGoal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('index'))

# Main entry point of the application
if __name__ == '__main__':
    with app.app_context():
        create_tables()  # Create tables within the application context
    app.run(debug=True, host='0.0.0.0', port=5001)
