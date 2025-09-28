from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from utils.roles import roles_required

ns = Namespace("users", description="用户管理相关接口")

# 数据模型定义
user_response_model = ns.model(
    "UserResponse",
    {
        "id": fields.Integer(description="用户ID"),
        "username": fields.String(description="用户名"),
        "email": fields.String(description="邮箱"),
        "role": fields.String(description="角色"),
        "created_at": fields.String(description="创建时间"),
    },
)


@ns.route("")
class UserListResource(Resource):
    @ns.doc("get_users")
    @jwt_required()
    @roles_required("interviewer", "admin")
    def get(self):
        """获取用户列表（面试官和管理员可见）"""
        try:
            # 获取查询参数
            role = request.args.get("role")

            # 构建查询
            query = User.query
            if role:
                query = query.filter(User.role == role)

            users = query.all()

            # 转换为字典格式
            users_data = []
            for user in users:
                users_data.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "created_at": (
                            user.created_at.isoformat() if user.created_at else None
                        ),
                    }
                )

            return {"data": users_data, "message": "获取用户列表成功"}, 200
        except Exception as e:
            return {"message": f"获取用户列表失败: {str(e)}"}, 500


@ns.route("/<int:user_id>")
class UserResource(Resource):
    @ns.doc("get_user")
    @jwt_required()
    @roles_required("interviewer", "admin")
    def get(self, user_id):
        """获取指定用户信息（面试官和管理员可见）"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {"message": "用户不存在"}, 404

            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }

            return {"data": user_data, "message": "获取用户信息成功"}, 200
        except Exception as e:
            return {"message": f"获取用户信息失败: {str(e)}"}, 500
