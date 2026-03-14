from . import inscripciones
from flask import render_template, request, redirect, url_for
import forms
from models import db
from flask import flash
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from inscripciones.routes import inscripciones, inscripciones
from models import Inscripcion, Alumnos, Curso, Maestros
from models import db

@inscripciones.route("/inscripcion", methods=["GET", "POST"])
def inscripcion():
    create_form = forms.InscripcionForm(request.form)
    res = db.session.query(Inscripcion, Alumnos, Curso, Maestros)\
        .join(Alumnos, Inscripcion.alumno_id == Alumnos.id)\
        .join(Curso, Inscripcion.curso_id == Curso.id)\
        .join(Maestros, Curso.maestro_id == Maestros.matricula)\
        .all()
    return render_template("inscripciones/listadoInscripciones.html", form = create_form, inscripciones = res)

@inscripciones.route("/inscripciones/insertar", methods=["GET", "POST"])
def insertar():
    create_form = forms.InscripcionForm(request.form)
    if request.method == "GET":
        alumnos = db.session.query(Alumnos).all()
        cursos = db.session.query(Curso).all()
        create_form.id_alumno.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]
        create_form.id_curso.choices = [(c.id, c.nombre) for c in cursos]

    if request.method == "POST":
        if not create_form.validate():
            for campo, errores in create_form.errors.items():
                for error in errores:
                    flash(f"{campo}: {error}", "error")
            return render_template("inscripciones/Inscripciones.html", form=create_form)
        alumno_sel = create_form.id_alumno.data
        curso_sel = create_form.id_curso.data

        inscripcion_existente = db.session.query(Inscripcion).filter(
            Inscripcion.alumno_id == alumno_sel,
            Inscripcion.curso_id == curso_sel
        ).first()

        if inscripcion_existente:
            flash("Este alumno ya se encuentra inscrito a este curso. Elija otro curso", "errors")
            return redirect(url_for("inscripciones.insertar"))
        else:
            nueva_inscripcion = Inscripcion(
                alumno_id = alumno_sel, 
                curso_id = curso_sel,
                fecha_incripcion = create_form.fecha_inscripcion.data
            )

            db.session.add(nueva_inscripcion)
            db.session.commit()

            flash("Inscripción registrada correctamente.", "success")
            return redirect(url_for("inscripciones.inscripcion"))
        
        return redirect(url_for("inscripciones.inscripcion"))
    return render_template("inscripciones/Inscripciones.html", form = create_form)

@inscripciones.route("/inscripciones/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.InscripcionForm(request.form)
    
    alumnos = db.session.query(Alumnos).all()
    cursos = db.session.query(Curso).all()
    create_form.id_alumno.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]
    create_form.id_curso.choices = [(c.id, c.nombre) for c in cursos]

    if request.method == "GET":
        id = request.args.get("id")
        inscripcion = db.session.query(Inscripcion).filter(Inscripcion.id == id).first()
        
        create_form.id_alumno.data = inscripcion.alumno_id
        create_form.id_curso.data = inscripcion.curso_id
        create_form.fecha_inscripcion.data = inscripcion.fecha_incripcion

    if request.method == "POST":
        if not create_form.validate():
            for campo, errores in create_form.errors.items():
                for error in errores:
                    flash(f"{campo}: {error}", "error")
            return render_template("inscripciones/modificar.html", form=create_form)
        
        id = request.args.get("id")
        inscripcion1 = db.session.query(Inscripcion).filter(Inscripcion.id == id).first()
        
        verificar_inscripcion = db.session.query(Inscripcion).filter(
            Inscripcion.alumno_id == create_form.id_alumno.data,
            Inscripcion.curso_id == create_form.id_curso.data,
            Inscripcion.id != inscripcion1.id
        ).first()

        if verificar_inscripcion is not None:
            flash("Ese alumno ya está inscrito en ese curso.", "error")
            return render_template("inscripciones/modificar.html", form=create_form)
        
        inscripcion1.alumno_id = create_form.id_alumno.data
        inscripcion1.curso_id = create_form.id_curso.data
        inscripcion1.fecha_incripcion = create_form.fecha_inscripcion.data

        db.session.add(inscripcion1)
        db.session.commit()
        
        return redirect(url_for("inscripciones.inscripcion"))
    return render_template("inscripciones/modificar.html", form = create_form)

@inscripciones.route("/inscripciones/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.InscripcionForm(request.form)
    
    alumnos = db.session.query(Alumnos).all()
    cursos = db.session.query(Curso).all()
    create_form.id_alumno.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]
    create_form.id_curso.choices = [(c.id, c.nombre) for c in cursos]

    if request.method == "GET":
        id = request.args.get("id")
        inscripcion = db.session.query(Inscripcion).filter(Inscripcion.id == id).first()
        
        create_form.id_alumno.data = inscripcion.alumno_id
        create_form.id_curso.data = inscripcion.curso_id
        create_form.fecha_inscripcion.data = inscripcion.fecha_incripcion 

    if request.method == "POST":
        id = request.args.get("id") 
        inscri = Inscripcion.query.get(id)
        
        db.session.delete(inscri)
        db.session.commit()
        
        return redirect(url_for("inscripciones.inscripcion"))
        
    return render_template("inscripciones/eliminar.html", form = create_form)

@inscripciones.route("/inscripciones/detalles", methods = ["GET", "POST"])
def detalle():
    create_form = forms.InscripcionForm(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        inscripcion = db.session.query(Inscripcion).filter(Inscripcion.id == id).first()
        id = request.args.get("id")
        
        alumno = db.session.query(Alumnos).filter(Alumnos.id == inscripcion.alumno_id).first()
        curso = db.session.query(Curso).filter(Curso.id == inscripcion.curso_id).first()

        nombre_alumno = alumno.nombre
        apellidos_alumno = alumno.apellidos
        nombre_curso = curso.nombre
        fecha = inscripcion.fecha_incripcion

    return render_template("inscripciones/detalles.html", id=id, nombre_alumno=nombre_alumno, apellidos_alumno=apellidos_alumno, nombre_curso=nombre_curso, fecha=fecha)