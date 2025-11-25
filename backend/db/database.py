"""
Database connection and setup for ResumeSense.
Converted from MySQL + PyMySQL → PostgreSQL + SQLAlchemy.
"""

import os
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float,
    DateTime, ForeignKey
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found. Add it in Render → Environment Variables.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    """Provide a DB session for API routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------
# TABLE MODELS (ORM)
# -----------------------------------

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    analysis_results = relationship("AnalysisResult", back_populates="resume")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analysis_results = relationship("AnalysisResult", back_populates="job")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"))
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"))

    match_score = Column(Float)
    ats_score = Column(Float)
    quality_score = Column(Float)

    ats_flags = Column(JSONB)
    power_verb_suggestions = Column(JSONB)
    match_details = Column(JSONB)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="analysis_results")
    job = relationship("Job", back_populates="analysis_results")


# -----------------------------------
# INIT DB (Create tables)
# -----------------------------------

def init_db():
    """Creates all tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL tables created successfully")
