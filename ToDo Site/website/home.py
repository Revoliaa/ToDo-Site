import re
from flask import Blueprint, render_template, request, jsonify
from flask.helpers import flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

homePage = Blueprint("homePage", __name__)

@homePage.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short.", category = "error")
        else:
            new_note = Note(text = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added.", category = "success")

    return render_template("home.html", user = current_user)

@homePage.route("/delete-note", methods = ["POST"])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})