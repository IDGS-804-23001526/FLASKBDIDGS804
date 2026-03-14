import forms
from models import Alumnos
from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_migrate import Migrate # Agregar referencia de migracion
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms 
from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos
from inscripciones.routes import inscripciones
from consultas.routes import consultas
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros) # Registrar el blueprint de maestros
app.register_blueprint(alumnos) # Registrar el blueprint de alumnos
app.register_blueprint(cursos) # Registrar el blueprint de cursos
app.register_blueprint(inscripciones) # Registrar el blueprint de inscripciones
app.register_blueprint(consultas)
db.init_app(app)
migrate = Migrate(app, db) # migracion a base de datos
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
    