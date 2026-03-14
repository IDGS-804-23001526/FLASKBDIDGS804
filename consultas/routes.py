from sqlalchemy.ext.asyncio import create_async_engine
from . import consultas
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from models import Curso, Maestros, Alumnos, Inscripcion

@consultas.route("/consultas", methods = ["GET", "POST"])
def detalle():
    create_form = forms.ConsultaForm(request.form)
    
    cursos = db.session.query(Curso).all()
    create_form.id_curso.choices = [(c.id, c.nombre) for c in cursos]

    alumnos_inscritos = []
    nombre_curso = "" 
    nombre_maestro = ""

    if request.method == "POST":
        id_curso_seleccionado = create_form.id_curso.data
        
        curso = db.session.query(Curso).filter(Curso.id == id_curso_seleccionado).first()
        if curso:
            nombre_curso = curso.nombre
            nombre_maestro = f"{curso.maestro.nombre} {curso.maestro.apellidos}"
        
        alumnos_inscritos = db.session.query(Alumnos)\
            .join(Inscripcion, Alumnos.id == Inscripcion.alumno_id)\
            .filter(Inscripcion.curso_id == id_curso_seleccionado)\
            .all()


    return render_template("consultas/consultas.html", form=create_form, alumnos_inscritos=alumnos_inscritos, nombre_curso=nombre_curso, nombre_maestro=nombre_maestro)

@consultas.route("/consulta_alumno", methods=["GET", "POST"])
def consulta_alumno():
    create_form = forms.ConsultaForm(request.form)

    alumnos = db.session.query(Alumnos).all()
    create_form.id_alumno.choices = [(a.id, a.nombre) for a in alumnos]

    alumno_seleccionado = None
    nombre_cursos = []
    nombre_maestro = ""
    
    if request.method == "POST":
        id_alumno_seleccionado = create_form.id_alumno.data

        alumno_seleccionado = db.session.query(Alumnos).filter(Alumnos.id == id_alumno_seleccionado).first()

        nombre_cursos = db.session.query(Curso).join(
            Inscripcion, Curso.id == Inscripcion.curso_id
        ).join(
            Maestros, Curso.maestro_id == Maestros.matricula
        ).filter(Inscripcion.alumno_id == id_alumno_seleccionado).all()
        redirect(url_for('consultas.consulta_alumno'))

    return render_template("consultas/consultas_alumno.html", form= create_form, alumno_seleccionado = alumno_seleccionado, nombre_cursos = nombre_cursos)

        