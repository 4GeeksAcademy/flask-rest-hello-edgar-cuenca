import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Follower(db.Model):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    
    # Relación para que el diagrama dibuje la conexión
    user = relationship("User")

class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum("video", "photo", name="media_type"), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


if __name__ == '__main__':
    from eralchemy2 import render_er
    try:
        # CAMBIO AQUÍ: Usamos db.metadata en lugar de db.Model
        render_er(db.metadata, 'diagram.png')
        print("¡Éxito! El archivo diagram.png se ha actualizado correctamente.")
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")
        # Tip adicional: Si te dice que falta una librería de sistema, 
        # intenta instalar: sudo apt-get install graphviz (si estás en Linux/Codespaces)