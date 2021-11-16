# Imports from Flask
from flask import Blueprint, render_template, flash, abort, url_for, redirect
# Extension for implementing Flask-Login for authentication
from flask_login import current_user, login_required
# Extension for implementing translations
from flask_babel import _
from flask_babel import lazy_gettext as _l
# Imports from the app package
from app import db
from app.models import Tour

from app.tour.forms import CreateTourForm, UpdateTourForm

tour = Blueprint("tour", __name__, template_folder="templates")

# Route for listing tours
@tour.route("/")
@login_required
def list():
    tours = Tour.query.all()
    return render_template("list_tours.html", tours=tours)

# Route for creating new tours
@tour.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreateTourForm()

    if form.validate_on_submit():
        title        = form.title.data
        artist       = form.artist.data
        description  = form.description.data
        genre        = form.genre.data
        start_date   = form.start_date.data
        end_date     = form.end_date.data

        tour = Tour(title, artist, description, genre, start_date, end_date, current_user.id)
        db.session.add(tour)
        db.session.commit()
        flash(_("The new tour has been added."), "success")
        return redirect(url_for("tour.show", slug=tour.slug))

    return render_template("create_tour.html", form=form)

# Route for updating a tour
@tour.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    form = UpdateTourForm()

    tour = Tour.query.filter_by(slug=slug).first()

    if not tour or not current_user.is_tour_owner(tour):
        flash(_("You are not authorized to do this."), "danger")
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        title       = form.title.data
        artist      = form.artist.data
        description = form.description.data
        genre       = form.genre.data
        start_date  = form.start_date.data
        end_date    = form.end_date.data

        tour.title       = title
        tour.artist      = artist
        tour.description = description
        tour.genre       = genre
        tour.start_date  = start_date
        tour.end_date    = end_date

        db.session.add(tour)
        db.session.commit()
        flash(_("The tour has been updated."), "success")
        return redirect(url_for("tour.show", slug=tour.slug))

    form.title.data       = tour.title
    form.artist.data      = tour.artist
    form.description.data = tour.description
    form.genre.data       = tour.genre
    form.start_date.data  = tour.start_date
    form.end_date.data    = tour.end_date
    return render_template("edit_tour.html", tour=tour, form=form)

# Route for deleting a tour
@tour.route("/delete/<slug>", methods=["POST"])
@login_required
def delete(slug):
    tour = Tour.query.filter_by(slug=slug).first()
    if not tour or not current_user.is_tour_owner(tour):
        flash(_("You are not authorized to do this."), "danger")
        return redirect(url_for("main.home"))
    db.session.delete(tour)
    db.session.commit()
    flash(_("The tour has been deleted."), "success")
    return redirect(url_for("main.home"))

# Route for showing a tour
@tour.route("/show/<slug>")
@login_required
def show(slug):
    tour = Tour.query.filter_by(slug=slug).first()
    if not tour:
        abort(404)
    return render_template("show_tour.html", tour=tour)
