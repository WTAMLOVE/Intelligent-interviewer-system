from extensions import db
from datetime import datetime


class InterviewEvaluation(db.Model):
    __tablename__ = "interview_evaluations"

    id = db.Column(db.Integer, primary_key=True)

    # 关联的面试ID
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)

    # 评价者ID（面试官）
    evaluator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 总分
    total_score = db.Column(db.Integer, nullable=False, default=0)

    # 满分
    max_score = db.Column(db.Integer, nullable=False, default=100)

    # 总体评价
    overall_comments = db.Column(db.Text, nullable=True)

    # 技能评价（JSON格式存储各项技能评分）
    skill_ratings = db.Column(db.JSON, nullable=True)

    # 综合建议
    recommendations = db.Column(db.Text, nullable=True)

    # 是否通过面试
    is_passed = db.Column(db.Boolean, nullable=False, default=False)

    # 评价是否已完成（锁定状态）
    is_finalized = db.Column(db.Boolean, nullable=False, default=False)

    # 通过/不通过的原因
    decision_reason = db.Column(db.Text, nullable=True)

    # 评价时间
    evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 更新时间
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 关联关系
    interview = db.relationship("Interview", backref="evaluation", uselist=False)
    evaluator = db.relationship("User", backref="evaluations")

    def to_dict(self):
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "evaluator_id": self.evaluator_id,
            "total_score": self.total_score,
            "max_score": self.max_score,
            "overall_comments": self.overall_comments,
            "skill_ratings": self.skill_ratings,
            "recommendations": self.recommendations,
            "is_passed": self.is_passed,
            "is_finalized": self.is_finalized,
            "decision_reason": self.decision_reason,
            "evaluated_at": (
                self.evaluated_at.isoformat() if self.evaluated_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # 包含评价者信息
            "evaluator": self.evaluator.to_dict() if self.evaluator else None,
        }

    def calculate_percentage(self):
        """计算得分百分比"""
        if self.max_score <= 0:
            return 0
        return round((self.total_score / self.max_score) * 100, 2)
