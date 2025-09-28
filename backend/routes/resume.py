from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.resume_service import ResumeService
from models.user import User
from utils.roles import roles_required

ns = Namespace("resumes", description="简历管理相关接口")

# 数据模型定义
resume_model = ns.model(
    "Resume",
    {
        "content": fields.String(required=True, description="简历内容（纯文本）"),
    },
)

resume_response_model = ns.model(
    "ResumeResponse",
    {
        "id": fields.Integer(description="简历ID"),
        "user_id": fields.Integer(description="用户ID"),
        "content": fields.String(description="简历内容"),
        "created_at": fields.String(description="创建时间"),
        "updated_at": fields.String(description="更新时间"),
    },
)


@ns.route("/my")
class MyResumeResource(Resource):
    @ns.doc("get_my_resume")
    @jwt_required()
    @roles_required("interviewee")
    def get(self):
        """获取我的简历"""
        current_user_id = get_jwt_identity()

        try:
            resume = ResumeService.get_resume_by_user_id(current_user_id)
            if not resume:
                return {"data": None, "message": "暂无简历"}, 200

            return {"data": resume.to_simple_dict(), "message": "获取简历成功"}, 200
        except Exception as e:
            return {"message": f"获取简历失败: {str(e)}"}, 500

    @ns.doc("create_or_update_my_resume")
    @ns.expect(resume_model)
    @jwt_required()
    @roles_required("interviewee")
    def post(self):
        """创建或更新我的简历"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        try:
            content = data.get("content", "")
            # 允许保存空的简历内容

            resume = ResumeService.create_or_update_resume(current_user_id, content)
            return {"data": resume.to_simple_dict(), "message": "简历保存成功"}, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": f"保存简历失败: {str(e)}"}, 500

    @ns.doc("delete_my_resume")
    @jwt_required()
    @roles_required("interviewee")
    def delete(self):
        """删除我的简历"""
        current_user_id = get_jwt_identity()

        try:
            ResumeService.delete_resume(current_user_id)
            return {"message": "简历删除成功"}, 200
        except ValueError as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {"message": f"删除简历失败: {str(e)}"}, 500


@ns.route("/user/<int:user_id>")
class UserResumeResource(Resource):
    @ns.doc("get_user_resume")
    @jwt_required()
    @roles_required("interviewer", "admin")
    def get(self, user_id):
        """获取指定用户的简历（面试官和管理员可见）"""
        try:
            resume = ResumeService.get_resume_by_user_id(user_id)
            if not resume:
                return {"message": "简历不存在"}, 404

            return {"data": resume.to_simple_dict(), "message": "获取简历成功"}, 200
        except Exception as e:
            return {"message": f"获取简历失败: {str(e)}"}, 500
