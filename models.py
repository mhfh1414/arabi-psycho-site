from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, JSON, ForeignKey

db = SQLAlchemy()

class PatientCase(db.Model):
    __tablename__ = "patient_case"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    sex: Mapped[str] = mapped_column(String(10), nullable=True)
    marital: Mapped[str] = mapped_column(String(20), nullable=True)
    contact: Mapped[str] = mapped_column(String(120), nullable=True)
    presenting_problem: Mapped[str] = mapped_column(Text, nullable=True)
    symptoms_text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime)

class TestResult(db.Model):
    __tablename__ = "test_result"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(Integer, ForeignKey("patient_case.id"), nullable=True)
    test_key: Mapped[str] = mapped_column(String(50))
    score_total: Mapped[int] = mapped_column(Integer)
    score_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped["DateTime"] = mapped_column(DateTime)
