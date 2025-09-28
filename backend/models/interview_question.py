from extensions import db
from datetime import datetime


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    id = db.Column(db.Integer, primary_key=True)

    # 关联的面试ID
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)

    # 题目内容
    question_text = db.Column(db.Text, nullable=False)

    # 题目类型: 'single_choice', 'multiple_choice', 'text', 'code'
    question_type = db.Column(db.String(32), nullable=False, default="text")

    # 选择题选项（JSON格式存储）
    options = db.Column(db.JSON, nullable=True)

    # 标准答案或参考答案
    reference_answer = db.Column(db.Text, nullable=True)

    # 题目分值
    score = db.Column(db.Integer, default=10)

    # 题目顺序
    order_index = db.Column(db.Integer, default=0)

    # 面试者的答案
    candidate_answer = db.Column(db.Text, nullable=True)

    # 面试官评分
    actual_score = db.Column(db.Integer, nullable=True)

    # 面试官评语
    comments = db.Column(db.Text, nullable=True)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 更新时间
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 关联关系
    interview = db.relationship("Interview", backref="questions")

    def to_dict(self):
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "reference_answer": self.reference_answer,
            "score": self.score,
            "order_index": self.order_index,
            "candidate_answer": self.candidate_answer,
            "actual_score": self.actual_score,
            "comments": self.comments,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_candidate_dict(self):
        """面试者视角的数据，不包含参考答案和评分"""
        return {
            "id": self.id,
            "interview_id": self.interview_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "score": self.score,
            "order_index": self.order_index,
            "candidate_answer": self.candidate_answer,
        }
