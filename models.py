from app import db

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    school = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(120), nullable=False)
    donation_amount = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'Donor {self.name}'
