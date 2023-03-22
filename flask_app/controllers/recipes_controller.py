from flask_app import app
from flask import Flask, render_template, redirect, request, session
from flask import flash
from pprint import pprint
from flask_app.models.users_model import User
from flask_app.models.recipe_model import Recipe


@app.route("/recipe/new")
def new_recipe():
    if 'logged_in_user_id' not in session:
        flash("Session timed-out, Please login Again !","login")
        return redirect("/")
    return render_template("new_recipe.html")

@app.route("/save_recipe", methods=['POST'])
def save_recipe():
    if 'logged_in_user_id' not in session:
        flash("Session timed-out, Please login Again !","login")
        return redirect("/")
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date_cooked" : request.form['date_cooked'],
        "under_30_min" : request.form['under_30_min'],
        "user_id" : session['logged_in_user_id']
    }
    results = Recipe.create_recipe(data)
    return redirect("/recipes")


@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    if 'logged_in_user_id' not in session:
        flash("Session timed-out, Please login Again !","login")
        return redirect("/")
    logged_in_user = User.get_user_by_id(session['logged_in_user_id'])
    recipe_detail = Recipe.get_one_recipe(id)
    return render_template("edit_recipe.html", recipe_detail = recipe_detail)

@app.route("/edit_my_recipe", methods=['POST'])
def edit():
    print(f"priting the request form values as {request.form}")
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipe/edit/{ request.form['id'] }")
    Recipe.edit_my_recipe(request.form)
    return redirect("/recipes")

@app.route("/recipe/<int:id>")
def show_recipe(id):
    if 'logged_in_user_id' not in session:
        flash("Session timed-out, Please login Again !","login")
        return redirect("/")
    logged_in_user = User.get_user_by_id(session['logged_in_user_id'])
    recipe_detail = Recipe.get_one_recipe(id)
    print(f'recipe details are {recipe_detail}')
    return render_template("show_recipe.html", first_name = logged_in_user.first_name, recipe_detail = recipe_detail)

@app.route("/delete/<int:id>")
def delete(id):
    Recipe.delete_recipe(id)
    return redirect("/recipes")
    
