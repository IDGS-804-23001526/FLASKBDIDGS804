from sqlalchemy.ext.asyncio import create_async_engine
from . import cursos
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from cursos.routes import cursos, cursos
from models import Curso, Maestros, Alumnos, Inscripcion

@cursos.route("/curso", methods=["GET", "POST"])
def curso():
    create_form = forms.CursoForm(request.form)
    cursos = Curso.query.all()
    return render_template("cursos/listadoCursos.html", form = create_form, cursos = cursos)

@cursos.route("/cursos/insertar", methods=["GET", "POST"])
def insertar():
    create_form = forms.CursoForm(request.form)
    maes = db.session.query(Maestros).all()
    create_form.id_maestro.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maes]

    if request.method == "POST":
        if not create_form.validate():
            return render_template("cursos/cursos.html", form=create_form)

        maestro_id = create_form.id_maestro.data
        curso_id = create_form.id.data

        curso_existente = db.session.query(Curso).filter(Curso.id == curso_id).first()
        maestro_ocupado = db.session.query(Curso).filter(Curso.maestro_id == maestro_id).first()

        if curso_existente is not None: 
            flash("Ese curso ya existe", "Error")
            return redirect(url_for("cursos.insertar"))

        if maestro_ocupado is not None:
            flash("El maestro ya tiene curso asignado", "error")
            return redirect(url_for("cursos.insertar"))

        

        curs = Curso(
            id = create_form.id.data,
            nombre = create_form.nombre.data,
            descripcion = create_form.descripcion.data,
            maestro_id = create_form.id_maestro.data
        )
        
        db.session.add(curs)
        db.session.commit()
        return redirect(url_for("cursos.curso"))
    return render_template("cursos/cursos.html", form = create_form)

@cursos.route("/cursos/detalles", methods = ["GET", "POST"])
def detalle():
    create_form = forms.CursoForm(request.form)

    alumnos_inscritos = []

    if request.method == "GET":
        id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        id = request.args.get("id")
        nombre = curso.nombre
        descripcion = curso.descripcion
        nombre_maestro = curso.maestro.nombre
        apellido_maestro = curso.maestro.apellidos

        alumnos_inscritos = db.session.query(Alumnos)\
            .join(Inscripcion, Alumnos.id == Inscripcion.alumno_id)\
            .filter(Inscripcion.curso_id == id)\
            .all()

        
    return render_template("cursos/detalles.html", id = id, nombre = nombre, descripcion = descripcion, nombre_maestro = nombre_maestro, apellido_maestro = apellido_maestro, alumnos_inscritos = alumnos_inscritos)


@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.CursoForm(request.form)
    maes = db.session.query(Maestros).all()
    create_form.id_maestro.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maes]

    if request.method == "GET":
        id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        id = request.args.get("id")
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.id_maestro.data = curso.maestro_id

    if request.method == "POST":
        id = create_form.id.data
        curs = Curso.query.get(id)
        db.session.delete(curs)
        db.session.commit()
        return redirect(url_for("cursos.curso"))
    return render_template("cursos/eliminar.html", form = create_form)

@cursos.route("/cursos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.CursoForm(request.form)
    maes = db.session.query(Maestros).all()
    create_form.id_maestro.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maes]

    if (request.method == "GET"):
        id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        id = request.args.get("id")
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.id_maestro.data = curso.maestro_id
    
    if request.method == "POST":
        id = request.args.get("id")
        curso1 = db.session.query(Curso).filter(Curso.id == id).first()
        curso1.id = id
        curso1.nombre = create_form.nombre.data
        curso1.descripcion = create_form.descripcion.data
        curso1.maestro_id = create_form.id_maestro.data

        db.session.add(curso1)
        db.session.commit()

        return redirect(url_for("cursos.curso"))
    return render_template("cursos/modificar.html", form = create_form)