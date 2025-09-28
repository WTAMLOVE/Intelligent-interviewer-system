from models.resume import Resume
from models.user import User
from extensions import db
from flask import current_app


class ResumeService:
    @staticmethod
    def get_resume_by_user_id(user_id):
        """根据用户ID获取简历"""
        return Resume.query.filter_by(user_id=user_id).first()

    @staticmethod
    def create_resume(user_id, content):
        """创建简历"""
        try:
            # 检查用户是否已有简历
            existing_resume = Resume.query.filter_by(user_id=user_id).first()
            if existing_resume:
                raise ValueError("用户已存在简历")

            # 检查用户是否存在且为面试者
            user = User.query.get(user_id)
            if not user:
                raise ValueError("用户不存在")
            if user.role != "interviewee":
                raise ValueError("只有面试者可以创建简历")

            resume = Resume(user_id=user_id, content=content)
            db.session.add(resume)
            db.session.commit()
            return resume
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"创建简历失败: {str(e)}")
            raise e

    @staticmethod
    def update_resume(user_id, content):
        """更新简历"""
        try:
            resume = Resume.query.filter_by(user_id=user_id).first()
            if not resume:
                raise ValueError("简历不存在")

            resume.content = content
            db.session.commit()
            return resume
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"更新简历失败: {str(e)}")
            raise e

    @staticmethod
    def delete_resume(user_id):
        """删除简历"""
        try:
            resume = Resume.query.filter_by(user_id=user_id).first()
            if not resume:
                raise ValueError("简历不存在")

            db.session.delete(resume)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"删除简历失败: {str(e)}")
            raise e

    @staticmethod
    def create_or_update_resume(user_id, content):
        """创建或更新简历"""
        existing_resume = Resume.query.filter_by(user_id=user_id).first()
        if existing_resume:
            return ResumeService.update_resume(user_id, content)
        else:
            return ResumeService.create_resume(user_id, content)
