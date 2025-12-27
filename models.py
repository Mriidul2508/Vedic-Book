from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Priest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False) # e.g., "Vedic", "Marriage"
    is_active = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='priest', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    ceremony_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True) # Indexed for faster search
    time_slot = db.Column(db.String(20), nullable=False) # e.g., "10:00 AM"
    status = db.Column(db.String(20), default="Pending") # Pending, Confirmed, Completed
    priest_id = db.Column(db.Integer, db.ForeignKey('priest.id'), nullable=True)

# Static data for the 16 Sanskars
SANSKARS = [
    {"name": "Garbhadhana", "purpose": "Conception", "age": "Pre-birth"},
    {"name": "Pumsavana", "purpose": "Fetus protection", "age": "3rd month pregnancy"},
    {"name": "Simantonnayana", "purpose": "Mental growth of child", "age": "7th month pregnancy"},
    {"name": "Jatakarma", "purpose": "Newborn welcoming", "age": "At birth"},
    {"name": "Namakarana", "purpose": "Naming ceremony", "age": "11th day"},
    {"name": "Nishkramana", "purpose": "First outing", "age": "4th month"},
    {"name": "Annaprashana", "purpose": "First solid food", "age": "6th month"},
    {"name": "Chudakarana", "purpose": "First haircut (Mundan)", "age": "1-3 years"},
    {"name": "Karnavedha", "purpose": "Ear piercing", "age": "3-5 years"},
    {"name": "Vidyarambha", "purpose": "Introduction to alphabet", "age": "5 years"},
    {"name": "Upanayana", "purpose": "Sacred thread", "age": "8-12 years"},
    {"name": "Vedarambha", "purpose": "Study of Vedas", "age": "After Upanayana"},
    {"name": "Keshanta", "purpose": "First shaving of beard", "age": "16 years"},
    {"name": "Samavartana", "purpose": "End of student life", "age": "~25 years"},
    {"name": "Vivaha", "purpose": "Marriage", "age": "Adult"},
    {"name": "Antyeshti", "purpose": "Funeral rites", "age": "Death"}
]