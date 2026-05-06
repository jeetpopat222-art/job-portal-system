from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@127.0.0.1:5432/job_portal_system"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------- USERS ---------------- #

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True)

    email: Mapped[str] = mapped_column(unique=True)

    password_hash: Mapped[str] = mapped_column()

    role: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # relationships
    seeker_profile = relationship("JobSeekerProfile", back_populates="user")

    employer_profile = relationship("EmployerProfile", back_populates="user")


# ---------------- JOB SEEKER PROFILE ---------------- #

class JobSeekerProfile(db.Model):
    __tablename__ = "job_seeker_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    full_name: Mapped[str] = mapped_column()

    skills: Mapped[str] = mapped_column()

    education: Mapped[str] = mapped_column()

    resume: Mapped[str] = mapped_column()

    # relationship
    user = relationship("User", back_populates="seeker_profile")

    applications = relationship("Application", back_populates="job_seeker")


# ---------------- EMPLOYER PROFILE ---------------- #

class EmployerProfile(db.Model):
    __tablename__ = "employer_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    company_name: Mapped[str] = mapped_column()

    company_description: Mapped[str] = mapped_column()

    website: Mapped[str] = mapped_column()

    # relationship
    user = relationship("User", back_populates="employer_profile")

    jobs = relationship("JobPosting", back_populates="employer")


# ---------------- JOB POSTING ---------------- #

class JobPosting(db.Model):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)

    employer_id: Mapped[int] = mapped_column(
        ForeignKey("employer_profiles.id")
    )

    title: Mapped[str] = mapped_column()

    description: Mapped[str] = mapped_column()

    salary: Mapped[int] = mapped_column()

    location: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # relationship
    employer = relationship("EmployerProfile", back_populates="jobs")

    applications = relationship("Application", back_populates="job")


# ---------------- APPLICATIONS ---------------- #

class Application(db.Model):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(
        ForeignKey("job_postings.id")
    )

    job_seeker_id: Mapped[int] = mapped_column(
        ForeignKey("job_seeker_profiles.id")
    )

    status: Mapped[str] = mapped_column(default="Pending")

    applied_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    # relationships
    job = relationship("JobPosting", back_populates="applications")

    job_seeker = relationship(
        "JobSeekerProfile",
        back_populates="applications"
    )


@app.route("/")
def home():
    return "COMING SOON"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)