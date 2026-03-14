from flask import Blueprint

consultas = Blueprint(
    "consultas", 
    __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes