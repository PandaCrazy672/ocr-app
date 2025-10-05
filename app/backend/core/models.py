from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, JSON, DateTime, func
import uuid
class Base(DeclarativeBase): pass
def uuid_str(): return str(uuid.uuid4())

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role = relationship("Role")

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="review")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

class Field(Base):
    __tablename__ = "fields"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    page: Mapped[int] = mapped_column(Integer)
    key: Mapped[str] = mapped_column(String(64))
    value: Mapped[str] = mapped_column(String(512))
    confidence: Mapped[float] = mapped_column(Float)
    bbox: Mapped[JSON] = mapped_column(JSON)

class Audit(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ts: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[str] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(64))
    document_id: Mapped[str] = mapped_column(String(36), nullable=True)
    meta: Mapped[JSON] = mapped_column(JSON, nullable=True)
