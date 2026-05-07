from flask import Flask,redirect,render_template,url_for,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey,URL
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@127.0.0.1:5432/Job_Portal_System"
db = SQLAlchemy(app)
app.secret_key = 'your-very-secret-key'



class User(db.Model):

    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role:Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    seeker_profile = relationship("Job_Seeker_Profiles", back_populates="user")

    employer_profile = relationship("Employer_Profiles", back_populates="user")



class Job_Seeker_Profiles(db.Model):

    __tablename__ = "job_seeker_profiles"

    id:Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    full_name:Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    education: Mapped[str] =mapped_column()
    resume: Mapped[str] = mapped_column()

    user = relationship("User", back_populates="seeker_profile")

    applications = relationship("Applications", back_populates="job_seeker")


class Employer_Profiles(db.Model):

    __tablename__ = "employer_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_name: Mapped[str] = mapped_column()
    company_description:Mapped[str] = mapped_column()
    website:Mapped[str] = mapped_column()

    user = relationship("User", back_populates="employer_profile")

    jobs = relationship("Job_Posting", back_populates="employer")


class Job_Posting(db.Model):

    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employer_profiles.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    salary: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()

    employer = relationship("Employer_Profiles", back_populates="jobs")

    applications = relationship("Applications", back_populates="job")


class Applications(db.Model):

    __tablename__ = "applications"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"))
    job_seeker_id: Mapped[int] = mapped_column(ForeignKey("job_seeker_profiles.id"))
    status: Mapped[str] = mapped_column()
    applied_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    

    job = relationship("Job_Posting", back_populates="applications")

    job_seeker = relationship(
        "Job_Seeker_Profiles",
        back_populates="applications"
    )

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("index.html")

@app.route("/signup",methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    hash_password = generate_password_hash(password)

    db.session.add(User(email=email,username=username,password_hash=hash_password,role=role))
    db.session.commit()
    
    return redirect(url_for("home"))

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash,password):
        session["user_id"] = user.id
        if user.role == "job_seeker":
            return redirect (url_for("job_seeker"))
        else: 
            return redirect (url_for("employer"))
    else:
        return "Invalid EMAIL or PASSWORD"

@app.route("/job_seeker")
def job_seeker():
    return render_template("job_seeker.html")


@app.route("/job_seeker_profile",methods=["POST","GET"])
def profile():
    if not session:
        return redirect (url_for("home"))
    if request.method == "POST":
        full_name = request.form.get("full_name")
        skills = request.form.get("skills")
        education = request.form.get("education")
        resume = request.form.get("resume")

        user_id = session.get("user_id")
        add_database = Job_Seeker_Profiles(full_name=full_name,skills=skills,education=education,resume=resume,user_id=user_id)
        db.session.add(add_database)
        db.session.commit()
        return redirect (url_for("job_seeker"))
    return render_template("job_seeker_profile.html")

@app.route("/job_seeker_logout")
def logout():
    session.clear()
    return redirect (url_for("home"))

@app.route("/employer")
def employer():
    return render_template("employer.html")

@app.route("/employer_profile",methods=["POST"])
def employer_profile():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        company_description = request.form.get("company_description")
        website = request.form.get("website")

        user_id = session.get("user_id")
        add_database = Employer_Profiles(company_description=company_description,company_name=company_name,website=website,user_id=user_id)
        db.session.add(add_database)
        db.session.commit()
    return render_template("employer_profile.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

