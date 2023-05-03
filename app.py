import os

from flask import Flask, request
from flask_restx.reqparse import RequestParser
from sqlalchemy.exc import IntegrityError

from trabalho.back_end.database import database
from trabalho.back_end.model.usuario import Usuario
from trabalho.back_end.schemas.usuario import UsuarioSchema, listar_usuario, listar_usuarios

from flask_cors import CORS

# from trabalho.back_end.model import Session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
database.init_app(app)  # inicializando Flask

with app.app_context():  # verificar se a base de dados está criada, caso contrario, criar;
    if "usuarios.db" not in os.listdir("./instance"):
        database.create_all()


# buscar usuario
@app.route("/buscar_usuario/<id_usuario>")
def buscar_user(id_usuario):
    usuario = database.session.query(Usuario).filter_by(id=id_usuario).first()
    return (usuario.json(), 200) if usuario else ({"msg": "Usuario nao encontrado."}, 400)


@app.route("/deletar/<id_usuario>", methods=['DELETE'])
def deletar_user(id_usuario):
    deletar = database.session.query(Usuario).filter_by(id=id_usuario).delete()

    database.session.commit()
    return (
        ({"msg": "Usuario Removido", "id": id_usuario}, 200)
        if deletar
        else
        ({"msg": "Usuario nao foi encontrado."},400))


@app.route("/cadastrar", methods=["POST"])
def cadastrar_user():  # forma -> atributo da função do tipo UsuarioSchema
    try:
        json = request.get_json(silent=True)
        if json and {'nome','email','saldo','idade'} <= json.keys():
            usuario = UsuarioSchema(**json)
            database.session.add(
                Usuario(nome=usuario.nome,email= usuario.email, idade=usuario.idade, saldo=usuario.saldo)
            )
            database.session.commit()
            return {"msg": "Usuario inserido com sucesso!"}, 200
        return {"msg": "Dados invalidos"}, 400
    except IntegrityError as e:
        error_msg = "Usuario ja existe na base"
        return {"msg": error_msg}, 409
    except Exception as e:
        error_msg = "Nao foi possivel adicionar o usuario."
        return {"msg": error_msg}, 404


@app.route("/visualizar", methods=["GET"])
def visualizar_users():
    usuarios = database.session.query(Usuario).all()

    if not usuarios:
        return {"usuarios": []}, 200
    else:
        return listar_usuarios(usuarios), 200


app.run(debug=True,port=5500)


