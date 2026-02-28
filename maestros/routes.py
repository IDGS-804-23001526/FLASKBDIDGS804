from . import maestros
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from maestros.routes import maestros, maestros
from models import Alumnos, Maestros

@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros", methods = ["GET", "POST"])
@maestros.route("/index")
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