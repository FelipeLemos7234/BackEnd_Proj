from pydantic import BaseModel
from typing import Optional,List
from trabalho.back_end.model.usuario import Usuario


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    idade: int
    saldo: int

class UsuarioBuscaSchema(BaseModel):

    nome: str = "John Doe"

class ListagemUsuariosSchema(BaseModel):

    produtos:List[UsuarioSchema]

class UsuarioViewSchema(BaseModel):

    id: int = 1
    nome: str = "John Doe"
    idade: int = 0
    saldo: int = 0

class UsuarioDelSchema(BaseModel):

    msg: str
    nome: str

def listar_usuarios(usuarios: List[Usuario]):

    arr = []

    for usuario in usuarios:

        arr.append({"nome":usuario.nome,
                    "email":usuario.email,
                    "idade":usuario.idade,
                    "saldo":usuario.saldo})

    return {"usuarios":arr}

def listar_usuario(usuario:Usuario):

    return {"id":usuario.id,
            "nome": usuario.nome,
            "email":usuario.email,
            "idade":usuario.idade,
            "saldo":usuario.saldo}
