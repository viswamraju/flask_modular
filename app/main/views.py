# Imports from Flask
from flask import Blueprint, render_template, current_app

main = Blueprint("main", __name__, template_folder="templates")

# Home route
@main.route("/")
def home():
	return render_template("home.html")

# 404 error handler
def page_not_found(e):
    return render_template("errors/404.html")

# Date formatting Jinja2 filter
@current_app.template_filter("date_format")
def date_format(value, format="%m/%d/%Y"):
    return value.strftime(format)
