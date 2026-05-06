from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey,URL
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime




app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@127.0.0.1:5432/Job_Portal_System"
db = SQLAlchemy(app)

class User(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role:Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Job_Seeker_Profiles(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    full_name:Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    education: Mapped[str] =mapped_column()
    resume: Mapped[str] = mapped_column()

class Employer_Profiles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    company_name: Mapped[str] = mapped_column()
    company_description:Mapped[str] = mapped_column()
    website:Mapped[str] = mapped_column()

class Job_Posting(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employer_profiles.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    salary: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()

class Applications(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_posting.id"))
    job_seeker_id: Mapped[int] = mapped_column(ForeignKey("job_seeker_profiles.id"))
    status: Mapped[str] = mapped_column()
    applied_at: Mapped[str] = mapped_column(default=datetime.utcnow)
    

@app.route("/")
def home():
    return "COMING SOON"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

