from sqlalchemy import Column, String, Integer, DateTime, Float
from trabalho.back_end.database import database


class Usuario(database.Model):  # criando tabela de usuarios

    id = Column("pk_usuario", Integer, primary_key=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True)
    idade = Column(Integer)
    saldo = Column(Float)

    # inicializar os atributos de um objeto assim que ele é formado
    # no caso, objeto = tabela 'Usuario'

    def __init__(self, nome: str, email: str, idade: int, saldo: int):
        self.nome = nome
        self.email = email
        self.idade = idade
        self.saldo = saldo

    def json(self) -> dict:
        return dict(
            nome=self.nome,
            email=self.email,
            idade=self.idade,
            saldo=self.saldo
        )
