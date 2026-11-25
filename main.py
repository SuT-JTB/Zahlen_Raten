from datetime import date
from sqlalchemy import (
    create_engine,
    text,
    inspect,
    insert,
    ForeignKey,
    String,
    select,
    Date,
    Float,
    Integer,
    String,
    Text,
    StaticPool,
)
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship

in_memory = True

if in_memory:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        "sqlite+pysqlite://highscores.db",
        echo=False,
        connect_args={"check_same_thread": False},
    )


class Base(DeclarativeBase):
    pass


class Highscore(Base):
    __tablename__ = "Highscores"

    Score_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    versuche: Mapped[int] = mapped_column(Integer)
    zeitpunkt: Mapped[date] = mapped_column(Date)


if not inspect(engine).get_table_names():
    Base.metadata.create_all(engine)
