from click.formatting import measure_table
from wtforms import SelectField
from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, IntegerField, RadioField, FloatField, DateField, DateTimeField
from wtforms import validators

class UserForm(Form):
    id = IntegerField('Id', [
        validators.number_range(min=1, max=20, message="Valor no valido")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=20, message="Requiere min 4 max 20")
    ])
    apellidos = StringField('apellidos', [
        validators.DataRequired(message="El apellido es requerido")
    ])
    email = EmailField('correo', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])
    telefono = IntegerField('telefono', [
        validators.DataRequired(message="El telefono es requerido"),
        validators.number_range(min=1, max=20, message="Valor no valido")
    ])

class MaestroForm(Form):
    matricula = IntegerField('Matricula', [
        validators.number_range(min=1, message="Valor no valido")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=20, message="Requiere min 4 max 20")
    ])
    apellidos = StringField('apellidos', [
        validators.DataRequired(message="El apellido es requerido")
    ])
    especialidad = StringField('Especialidad', [
        validators.DataRequired(message="El telefono es requerido")
    ])
    email = EmailField('correo', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])

class CursoForm(Form):
    id = IntegerField('Id Curso', [
        validators.data_required(message="El id es requerido")
    ])

    nombre = StringField('Nombre del curso', [
        validators.DataRequired(message="El nombre es requerido")
    ])

    descripcion = StringField('Descripción', [
        validators.DataRequired(message="La descripción es requerida")
    ])

    id_maestro = SelectField('Maestro', coerce=int, validators=[
        validators.DataRequired(message="El maestro es requerido")
    ])

class InscripcionForm(Form):
    id_alumno = SelectField('Alumno', coerce=int, validators=[
        validators.DataRequired(message="El alumno es requerido")
    ])

    id_curso = SelectField('Curso', coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un curso")
    ])

    fecha_inscripcion = DateTimeField('Fecha inscripcion', format="%Y-%m-%dT%H:%M") 

class ConsultaForm(Form):
    id_curso = SelectField('Curso', coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un curso")
    ])

    id_alumno = SelectField('Alumno', coerce=int, validators=[
        validators.DataRequired(message="Debe seleccionar un alumno")
    ])