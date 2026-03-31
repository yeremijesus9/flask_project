from app.core.extensions import db
from app.api.auth.models import Users

class UsersProfile(db.Model):
    __tablename__ = 'users_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    
    user = db.relationship('Users', backref=db.backref('profile', uselist=False))
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "color": self.color
        }
    
    def __repr__(self):
        return f'<UsersProfile {self.name}>'