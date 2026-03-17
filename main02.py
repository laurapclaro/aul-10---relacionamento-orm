from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker,relationship

Base = declarative_base()

#Sistema de uma rede de restaurantes
#Um restaurante tem varios pratos
#Cada prato pertence a apenas um retaurante

class Restaurante(Base):
    __tablename__ = "restaurantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=True)
    def __repr__(self):
        return f"- Restaurante = id: {self.id} - nome: {self.nome}"
    
class Prato(Base):
    __tablename__ = "pratos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String(50))

    restaurante_id = Column(Integer, ForeignKey("restaurantes.id"))
    restaurante = relationship("Restaurante", back_populates="pratos")

    def __repr__(self):
        return f"- Prato = id: {self.id} - nome: {self.nome} - preço: {self.preco}"
    


#Conexao com db

engine = create_engine("sqlite:///restaurantes.db")
Base.metadata.ceate_all(engine)
Session = sessionmaker(bind=engine)

def cadastrar():
    nome_restaurante1 = input("Digite o nome do restaurante: ").capitalize()
    nome_restaurante2 = input("Digite o nome do restaurante: ").capitalize()

    prato1 = input("Digite o nome do prato 1: ").capitalize()
    prato2 = input("Digite o nome do prato 2: ").capitalize()
    prato3 = input("Digite o nome do prato 3: ").capitalize()

    with Session() as session:
        try:
            cantina = Restaurante(nome=nome_restaurante1, cidade="Sao Paulo") 
            sushi = Restaurante(nome=nome_restaurante2, cidades="Santa Catarina")

            #pratos opção 1 vincular pelo atributo nome
            prato_cantina1 = Prato(nome=prato2,
                                   preco=float(input("Digite o preco: ")),
                                   categoria=input("Digite a categoria do prato: "),
                                   restaurante=cantina)
            prato_cantina2 = Prato(nome=prato2,
                                   preco=float(input("Digite o preco: ")),
                                   categoria=input("Digite a categoria do prato: "),
                                   restaurante=cantina)
            
            #pratos opção 2 vinculas pelo append()
            prato_sushi = Prato(
                nome=prato3,
                preco=float(input('Digite o preço: '),
                categoria=input("Digite a categoria do prato: ")          )

            )
            sushi.pratos.appen(prato_sushi)
            session.add_all([cantina, sushi])


            session.commit()
            print("Restaurante e pratos cadastrados!")
            






            pass
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro{erro}")

cadastrar()
def atualizar():
    with Session() as session:
        try:
            pudim = session.query(Prato).filter_by(nome="Pudim de leite").first()
            sushi = session.query(Prato).filter_by(nome="Sushi do bom").first()
            print(f"\nAntes - Pudim pertence a {pudim.restaurante.nome}")
            pudim.restaurante = sushi
            session.commit()
            print(f"\nDepois - Pudim pertence a {pudim.restaurante.nome}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro{erro}")

#Atualizar()
def deletar():
    with Session() as session:
        try:
            buscar_restaurante = session.query(Restaurante).filter_by(nome="Sushi do bom").first()
            session.delete(buscar_restaurante)
            session.commit()
            print("Restaurate deletado")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

deletar()



