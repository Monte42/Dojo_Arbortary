from belt_app import app
from flask import redirect, flash, session
from belt_app.models import visitor,tree




# ==============
# CREATE ROUTES
# ==============
@app.route('/visited/<int:id>')
def visit_tree(id):
    if not session.get('user_id'): return redirect('/')
    if not tree.Tree.fetch_tree_by_id(id):
        flash('This tree does not exist')
        return redirect('/dashboard')
    if visitor.Visitor.did_user_visit_tree_already(id):
        flash('You have visited this tree already')
        return redirect(f'/show/{id}')
    visitor.Visitor.create_new_visit(id)
    return redirect(f'/show/{id}')
