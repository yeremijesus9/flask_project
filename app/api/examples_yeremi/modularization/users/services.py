from app.extensions import db
from app.api.examples_yeremi.modularization.users.models import UsersProfile
from app.api.auth.models import Users

class UserService:
    @staticmethod
    def get_users():
        profiles = UsersProfile.query.all()
        return [profile.to_dict() for profile in profiles]
    
    @staticmethod
    def get_user_by_id(profile_id):
        profile = UsersProfile.query.get(profile_id)
        if not profile:
            return None
        return profile.to_dict()
    
    @staticmethod
    def get_user_by_user_id(user_id):
        profile = UsersProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return None
        return profile.to_dict()
    
    @staticmethod
    def create_user(user_id, name, role, color):
        existing_profile = UsersProfile.query.filter_by(user_id=user_id).first()
        if existing_profile:
            raise ValueError(f"User profile for user_id {user_id} already exists")
        
        user = Users.query.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} does not exist")
        
        profile = UsersProfile(user_id=user_id, name=name, role=role, color=color)
        db.session.add(profile)
        db.session.commit()
        return profile.to_dict()
    
    @staticmethod
    def update_user(profile_id, data):
        profile = UsersProfile.query.get(profile_id)
        if not profile:
            return None
        
        if 'name' in data:
            profile.name = data['name']
        if 'role' in data:
            profile.role = data['role']
        if 'color' in data:
            profile.color = data['color']
        
        db.session.commit()
        return profile.to_dict()
    
    @staticmethod
    def delete_user(profile_id):
        profile = UsersProfile.query.get(profile_id)
        if not profile:
            return False
        
        db.session.delete(profile)
        db.session.commit()
        return True
    
    @staticmethod
    def get_summary():
        total = UsersProfile.query.count()
        roles = db.session.query(UsersProfile.role).distinct().all()
        return {
            "total_users": total,
            "roles": [r[0] for r in roles]
        }