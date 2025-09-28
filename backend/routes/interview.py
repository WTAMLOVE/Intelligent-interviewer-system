from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.interview_service import InterviewService
from models.user import User
from utils.roles import roles_required

ns = Namespace("interviews", description="面试管理相关接口")

# 数据模型定义
interview_model = ns.model(
    "Interview",
    {
        "title": fields.String(required=True, description="面试标题"),
        "description": fields.String(description="面试描述"),
        "job_requirement_id": fields.Integer(required=True, description="岗位需求ID"),
        "interviewee_id": fields.Integer(description="面试者ID"),
        "duration_minutes": fields.Integer(description="预期时长(分钟)", default=60),
    },
)

question_model = ns.model(
    "Question",
    {
        "question_text": fields.String(required=True, description="题目内容"),
        "question_type": fields.String(
            description="题目类型",
            enum=["single_choice", "multiple_choice", "text", "code"],
            default="text",
        ),
        "options": fields.Raw(description="选择题选项(JSON)"),
        "reference_answer": fields.String(description="参考答案"),
        "score": fields.Integer(description="分值", default=10),
    },
)

evaluation_model = ns.model(
    "Evaluation",
    {
        "total_score": fields.Integer(required=True, description="总分"),
        "max_score": fields.Integer(description="满分", default=100),
        "overall_comments": fields.String(description="总体评价"),
        "skill_ratings": fields.Raw(description="技能评分(JSON)"),
        "recommendations": fields.String(description="综合建议"),
        "is_passed": fields.Boolean(required=True, description="是否通过"),
        "decision_reason": fields.String(description="决定原因"),
    },
)


@ns.route("/")
class InterviewList(Resource):
    @jwt_required()
    @roles_required("interviewer", "admin")
    def get(self):
        """获取面试列表"""
        current_user_id = int(get_jwt_identity())  # 转换为整数
        status = request.args.get("status")

        interviews, error = InterviewService.get_interviews_by_interviewer(
            current_user_id, status
        )
        if error:
            return {"message": error}, 400

        return {"data": interviews}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(interview_model)
    def post(self):
        """创建面试"""
        current_user_id = int(get_jwt_identity())  # 转换为整数
        data = request.get_json()

        # 设置创建者为当前用户
        data["interviewer_id"] = current_user_id

        interview, error = InterviewService.create_interview(data)
        if error:
            return {"message": error}, 400

        return {"data": interview, "message": "面试创建成功"}, 201


@ns.route("/<int:interview_id>")
class InterviewDetail(Resource):
    @jwt_required()
    @roles_required("interviewer", "interviewee", "admin")
    def get(self, interview_id):
        """获取面试详情"""
        current_user_id = int(get_jwt_identity())  # 转换为整数

        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        # 检查权限：面试官、面试者或管理员
        current_user = User.query.get(current_user_id)

        # 调试信息
        print(f"权限检查 - 当前用户ID: {current_user_id}, 角色: {current_user.role}")
        print(
            f"面试信息 - 面试官ID: {interview['interviewer_id']}, 面试者ID: {interview['interviewee_id']}"
        )

        # 管理员可以访问所有面试
        if current_user.role == "admin":
            pass
        # 面试官可以访问自己创建的面试
        elif interview["interviewer_id"] == current_user_id:
            pass
        # 面试者可以访问分配给自己的面试（但不能查看草稿状态）
        elif interview["interviewee_id"] == current_user_id:
            if interview["status"] == "draft":
                return {"message": "该面试尚未派发，暂时无法查看"}, 403
        else:
            return {"message": "无权限访问此面试"}, 403

        return {"data": interview}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(interview_model)
    def put(self, interview_id):
        """更新面试信息"""
        current_user_id = int(get_jwt_identity())  # 转换为整数
        data = request.get_json()

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
        ):
            return {"message": "无权限修改此面试"}, 403

        updated_interview, error = InterviewService.update_interview(interview_id, data)
        if error:
            return {"message": error}, 400

        return {"data": updated_interview, "message": "面试更新成功"}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    def delete(self, interview_id):
        """删除面试"""
        current_user_id = int(get_jwt_identity())  # 转换为整数

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)

        # 调试信息
        print(
            f"删除权限检查 - 当前用户ID: {current_user_id}, 角色: {current_user.role}"
        )
        print(f"面试信息 - 面试官ID: {interview['interviewer_id']}")

        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
        ):
            return {"message": "无权限删除此面试"}, 403

        success, error = InterviewService.delete_interview(interview_id)
        if error:
            return {"message": error}, 400

        return {"message": "面试删除成功"}, 200


@ns.route("/<int:interview_id>/assign")
class InterviewAssign(Resource):
    @jwt_required()
    @roles_required("interviewer", "admin")
    def post(self, interview_id):
        """分配面试给面试者"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        interviewee_id = data.get("interviewee_id")

        if not interviewee_id:
            return {"message": "请提供面试者ID"}, 400

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
        ):
            return {"message": "无权限分配此面试"}, 403

        updated_interview, error = InterviewService.assign_interview(
            interview_id, interviewee_id
        )
        if error:
            return {"message": error}, 400

        return {"data": updated_interview, "message": "面试分配成功"}, 200


@ns.route("/<int:interview_id>/questions")
class InterviewQuestions(Resource):
    @jwt_required()
    @roles_required("interviewer", "interviewee", "admin")
    def get(self, interview_id):
        """获取面试题目"""
        current_user_id = int(get_jwt_identity())

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
            and interview["interviewee_id"] != current_user_id
        ):
            return {"message": "无权限访问此面试题目"}, 403

        # 面试者只能看到适合的题目内容
        for_candidate = current_user.role == "interviewee"
        questions, error = InterviewService.get_interview_questions(
            interview_id, for_candidate
        )
        if error:
            return {"message": error}, 400

        return {"data": questions}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(question_model)
    def post(self, interview_id):
        """添加面试题目"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
        ):
            return {"message": "无权限添加题目"}, 403

        question, error = InterviewService.add_question(interview_id, data)
        if error:
            return {"message": error}, 400

        return {"data": question, "message": "题目添加成功"}, 201


@ns.route("/questions/<int:question_id>")
class QuestionDetail(Resource):
    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(question_model)
    def put(self, question_id):
        """更新题目"""
        data = request.get_json()

        question, error = InterviewService.update_question(question_id, data)
        if error:
            return {"message": error}, 400

        return {"data": question, "message": "题目更新成功"}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    def delete(self, question_id):
        """删除题目"""
        success, error = InterviewService.delete_question(question_id)
        if error:
            return {"message": error}, 400

        return {"message": "题目删除成功"}, 200


@ns.route("/questions/<int:question_id>/answer")
class QuestionAnswer(Resource):
    @jwt_required()
    @roles_required("interviewee", "admin")
    def post(self, question_id):
        """提交答案"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        answer = data.get("answer")

        if not answer:
            return {"message": "请提供答案"}, 400

        # 验证权限：只有当前面试的面试者可以提交答案
        from models.interview_question import InterviewQuestion
        from models.interview import Interview

        question = InterviewQuestion.query.get(question_id)
        if not question:
            return {"message": "题目不存在"}, 404

        interview = Interview.query.get(question.interview_id)
        if not interview:
            return {"message": "面试不存在"}, 404

        # 检查权限
        current_user = User.query.get(current_user_id)
        if current_user.role != "admin" and interview.interviewee_id != current_user_id:
            return {"message": "无权限提交此题目答案"}, 403

        # 检查面试状态
        if interview.status not in ["assigned", "in_progress"]:
            return {"message": "面试状态不允许提交答案"}, 400

        question, error = InterviewService.submit_answer(question_id, answer)
        if error:
            return {"message": error}, 400

        return {"data": question, "message": "答案提交成功"}, 200


@ns.route("/questions/<int:question_id>/score")
class QuestionScore(Resource):
    @jwt_required()
    @roles_required("interviewer", "admin")
    def post(self, question_id):
        """为题目评分"""
        data = request.get_json()
        score = data.get("score")
        comments = data.get("comments", "")

        if score is None:
            return {"message": "请提供分数"}, 400

        question, error = InterviewService.score_question(question_id, score, comments)
        if error:
            return {"message": error}, 400

        return {"data": question, "message": "评分成功"}, 200


@ns.route("/<int:interview_id>/evaluation")
class InterviewEvaluations(Resource):
    @jwt_required()
    @roles_required("interviewer", "interviewee", "admin")
    def get(self, interview_id):
        """获取面试评价"""
        current_user_id = int(get_jwt_identity())

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
            and interview["interviewee_id"] != current_user_id
        ):
            return {"message": "无权限查看此面试评价"}, 403

        evaluation, error = InterviewService.get_evaluation(interview_id)
        if error:
            return {"message": error}, 404

        return {"data": evaluation}, 200

    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(evaluation_model)
    def post(self, interview_id):
        """创建面试评价"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        # 检查权限
        interview, error = InterviewService.get_interview_by_id(interview_id)
        if error:
            return {"message": error}, 404

        current_user = User.query.get(current_user_id)
        if (
            current_user.role != "admin"
            and interview["interviewer_id"] != current_user_id
        ):
            return {"message": "无权限评价此面试"}, 403

        evaluation, error = InterviewService.create_evaluation(
            interview_id, current_user_id, data
        )
        if error:
            return {"message": error}, 400

        return {"data": evaluation, "message": "评价创建成功"}, 201


@ns.route("/evaluation/<int:evaluation_id>")
class EvaluationDetail(Resource):
    @jwt_required()
    @roles_required("interviewer", "admin")
    @ns.expect(evaluation_model)
    def put(self, evaluation_id):
        """更新面试评价"""
        data = request.get_json()

        evaluation, error = InterviewService.update_evaluation(evaluation_id, data)
        if error:
            return {"message": error}, 400

        return {"data": evaluation, "message": "评价更新成功"}, 200


# 面试者专用接口
@ns.route("/my-interviews")
class MyInterviews(Resource):
    @jwt_required()
    @roles_required("interviewee")
    def get(self):
        """获取我的面试列表"""
        current_user_id = int(get_jwt_identity())
        status = request.args.get("status")

        interviews, error = InterviewService.get_interviews_by_interviewee(
            current_user_id, status
        )
        if error:
            return {"message": error}, 400

        return {"data": interviews}, 200


@ns.route("/<int:interview_id>/start")
class InterviewStart(Resource):
    @jwt_required()
    @roles_required("interviewee")
    def post(self, interview_id):
        """开始面试"""
        current_user_id = int(get_jwt_identity())

        interview, error = InterviewService.start_interview(
            interview_id, current_user_id
        )
        if error:
            return {"message": error}, 400

        return {"data": interview, "message": "面试已开始"}, 200


@ns.route("/<int:interview_id>/complete")
class InterviewComplete(Resource):
    @jwt_required()
    @roles_required("interviewee")
    def post(self, interview_id):
        """完成面试"""
        current_user_id = int(get_jwt_identity())

        interview, error = InterviewService.complete_interview(
            interview_id, current_user_id
        )
        if error:
            return {"message": error}, 400

        return {"data": interview, "message": "面试已完成，感谢您的参与！"}, 200


@ns.route("/<int:interview_id>/status")
class InterviewStatus(Resource):
    @jwt_required()
    @roles_required("interviewer")
    def put(self, interview_id):
        """更新面试状态"""
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        if not data or "status" not in data:
            return {"message": "请提供要更新的状态"}, 400

        new_status = data["status"]

        # 验证状态值
        valid_statuses = ["draft", "assigned", "in_progress", "completed", "evaluated"]
        if new_status not in valid_statuses:
            return {
                "message": f"无效的状态值，必须是：{', '.join(valid_statuses)}"
            }, 400

        interview, error = InterviewService.update_interview_status(
            interview_id, new_status, current_user_id
        )
        if error:
            return {"message": error}, 400

        return {"data": interview, "message": f"面试状态已更新为：{new_status}"}, 200
