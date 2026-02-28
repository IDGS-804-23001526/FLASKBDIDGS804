from . import maestros
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from maestros.routes import maestros, maestros
from models import Maestros
from models import db

@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros", methods = ["GET", "POST"])
def index():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form = create_form, maestros = maestros)   

@maestros.route("/detalles", methods = ["GET", "POST"]) 
def detalles():
    create_form = forms.UserForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        matricula = request.args.get("matricula")
        nombre = maes1.nombre
        apellidos = maes1.apellidos
        especialidad = maes1.especialidad
        email = maes1.email

    return render_template("maestros/detalles.html", matricula = matricula, nombre = nombre, apellidos = apellidos, especialidad = especialidad, email = email) 

@maestros.route("/MaestroInsert", methods=["GET", "POST"])
def maestroInsert():
    create_form = forms.MaestroForm(request.form)
    if request.method == "POST":
        maes = Maestros(
        matricula = create_form.matricula.data,
        nombre = create_form.nombre.data,
        apellidos = create_form.apellidos.data,
        especialidad = create_form.especialidad.data,
        email = create_form.email.data)

        db.session.add(maes)
        db.session.commit()
        return redirect(url_for("maestros.index"))
    return render_template("maestros/Maestros.html", form = create_form)

@maestros.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        matricula = request.args.get("matricula")
        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
    
    if request.method == "POST":
        matricula = request.args.get("matricula")
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        maes1.matricula = matricula
        maes1.nombre = create_form.nombre.data
        maes1.apellidos = create_form.apellidos.data
        maes1.especialidad = create_form.especialidad.data
        maes1.email = create_form.email.data

        db.session.add(maes1)
        db.session.commit()
        return redirect(url_for("maestros.index"))
    return render_template("maestros/modificar.html", form = create_form)

@maestros.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.MaestroForm(request.form)
    
    if request.method == "GET":
        matricula = request.args.get("matricula")
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        matricula = request.args.get("matricula")
        
        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
    
    if request.method == "POST":
        matricula = create_form.matricula.data
        maes = Maestros.query.get(matricula)
        db.session.delete(maes)
        db.session.commit()
        return redirect(url_for("maestros.index"))
    return render_template("maestros/eliminar.html", form = create_form)


