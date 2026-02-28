from alumnos import alumnos
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from alumnos.routes import alumnos, alumnos
from models import Alumnos
from models import db

@alumnos.route("/alumn", methods = ["GET", "POST"])
def index():
    create_form = forms.UserForm(request.form)

    alumnos = Alumnos.query.all()
    return render_template("alumnos/index.html", create_form = create_form, alumnos = alumnos)

@alumnos.route("/Alumnos", methods = ["GET", "POST"])
def alumnoss():
    create_form = forms.UserForm(request.form)
    if request.method == "POST":
        alum = Alumnos(nombre = create_form.nombre.data,
        apellidos = create_form.apellidos.data,
        email = create_form.email.data,
        telefono = create_form.telefono.data)


        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("alumnos.index"))
    return render_template("alumnos/Alumnos.html", form = create_form)

@alumnos.route("/detalles", methods = ["GET", "POST"])
def detalles():
    create_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")

        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get("id")
        nombre = alum1.nombre
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono

    return render_template("alumnos/detalles.html", id = id, nombre = nombre, apellidos = apellidos, email = email, telefono = telefono)

@alumnos.route("/modificar", methods = ["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get("id")
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == "POST":
        id = request.args.get("id")
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.id = id
        alum1.nombre = create_form.nombre.data
        alum1.apellidos = create_form.apellidos.data
        alum1.email = create_form.email.data
        alum1.telefono = create_form.telefono.data

        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for("alumnos.index"))
    return render_template("alumnos/modificar.html", form = create_form)

@alumnos.route("/eliminar", methods = ["GET", "POST"])
def eliminar():
    create_form = forms.UserForm(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get("id")
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == "POST":
        id = create_form.id.data
        alum = Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for("alumnos.index"))
    return render_template("alumnos/eliminar.html", form = create_form)
