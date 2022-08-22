from belt_app import app
from flask import render_template, redirect, request,flash, session
from belt_app.models import tree


# =============
#  CREATE ROUTE
# =============
@app.route('/new/tree', methods=['GET','POST'])
def create_new_tree():
    if not session.get('user_id'): return redirect('/')
    if request.method == 'GET':return render_template('trees/create_tree.html', data=None)
    if tree.Tree.create_tree(request.form): return redirect('/dashboard')
    return render_template('trees/create_tree.html', data=request.form)


# ===========
# READ ROUTE
# ===========
@app.route('/dashboard')
def show_all():
    if not session.get('user_id'): return redirect('/')
    all_trees = tree.Tree.fetch_all_trees()
    return render_template('trees/all_trees.html', trees=all_trees)

@app.route('/show/<int:id>')
def show_single_tree(id):
    if not session.get('user_id'): return redirect('/')
    this_tree = tree.Tree.fetch_tree_by_id(id)
    if not this_tree:
        flash('This tree does not exist')
        return redirect('/dashboard')
    return render_template('trees/single_tree.html',tree=this_tree)



# ============
# UPDATE ROUTE
# ============
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_tree(id):
    if not session.get('user_id'):return redirect('/')
    if request.method == 'GET':
        this_tree = tree.Tree.fetch_tree_by_id(id)
        if not this_tree:
            flash('This tree does not exist')
            return redirect('/dashboard')
        if this_tree.user_id == session['user_id']:return render_template('trees/edit_tree.html', data=this_tree)
        flash('You are not authorized to do that!')
        return redirect('/dashboard')
    if tree.Tree.update_tree(request.form,id):return redirect(f'/show/{id}')
    return redirect(f'/edit/{id}')



# ============
# DELETE ROUTE
# ============
@app.route('/delete/<int:id>')
def delete_tree(id):
    if not session.get('user_id'):return redirect('/')
    this_tree = tree.Tree.fetch_tree_by_id(id)
    if not this_tree:
            flash('This tree does not exist...')
            return redirect('/dashboard')
    if this_tree.user_id != session['user_id']:
        flash('You are not authorized to do that!')
        return redirect('/dashboard')
    tree.Tree.delete_tree(id)
    return redirect('/user/account')
