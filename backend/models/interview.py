from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # 关联的岗位ID
    job_requirement_id = db.Column(
        db.Integer, db.ForeignKey("job_requirements.id"), nullable=False
    )

    # 面试官ID（创建该面试的面试官）
    interviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 面试者ID（可以为空，表示还未分配面试者）
    interviewee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # 面试状态: 'draft', 'assigned', 'in_progress', 'completed', 'evaluated'
    status = db.Column(db.String(32), nullable=False, default="draft")

    # 面试题数量
    question_count = db.Column(db.Integer, default=5)

    # 面试开始时间（面试者开始答题的时间）
    started_at = db.Column(db.DateTime, nullable=True)

    # 面试完成时间（面试者完成答题的时间）
    completed_at = db.Column(db.DateTime, nullable=True)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 更新时间
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 关联关系
    job_requirement = db.relationship("JobRequirement", backref="interviews")
    interviewer = db.relationship(
        "User", foreign_keys=[interviewer_id], backref="created_interviews"
    )
    interviewee = db.relationship(
        "User", foreign_keys=[interviewee_id], backref="assigned_interviews"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "job_requirement_id": self.job_requirement_id,
            "interviewer_id": self.interviewer_id,
            "interviewee_id": self.interviewee_id,
            "status": self.status,
            "question_count": self.question_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # 包含关联数据
            "job_requirement": (
                self.job_requirement.to_dict() if self.job_requirement else None
            ),
            "interviewer": self.interviewer.to_dict() if self.interviewer else None,
            "interviewee": self.interviewee.to_dict() if self.interviewee else None,
        }

    def to_simple_dict(self):
        """简化版本，不包含关联数据，避免循环引用"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "job_requirement_id": self.job_requirement_id,
            "interviewer_id": self.interviewer_id,
            "interviewee_id": self.interviewee_id,
            "status": self.status,
            "question_count": self.question_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
