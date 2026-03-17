from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker,relationship

#Criar base da classe
Base = declarative_base()

#Tabela do banco:
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))

    #Relacionamnto com pedidos
    pedidos = relationship("Pedido", back_populates="usuario")
    def __repr__(self):
        return f"Usuario - id={self.id}, nome={self.nome}"
    
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String(150))

    usuario_id = Column(Integer, ForeignKey("usuario.id"))  
    #ForeignKey tem mais numeros, muitos

    #Relacionamento
    usuario = relationship("Usuario", back_populates="pedidos")

    def _repr__(self):
        return f"Pedido - id={self.id}, produto={self.produto}"
    


#conexao c db

engine = create_engine("sqlite:///loja.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

#Criar u m usuario - objeto
usuario1 = Usuario(nome="Gabriel")

#Criar os pedidos

pedido1 = Pedido(produto="Iphone 17")
pedido2 = Pedido(produto="Notebook")

#Associando pedidos ao usuario

usuario1.pedidos.append(pedido1)
usuario1.pedidos.append(pedido2)


#salvar no banco

session.add(usuario1)
session.commit()

print(f"Usuario cadastrados: {usuario1.nome}")

todos_usuarios = session.query(Usuario).all()
for usuario in todos_usuarios:
    print(f"\nNome: {usuario.nome} ")
    for pedido in usuario.pedidos:
        print(f"Pedidos: {pedido.produto}")
