from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class JobRequirement(db.Model):
    __tablename__ = "job_requirements"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    skills = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "job_title": self.job_title,
            "description": self.description,
            "skills": self.skills,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
