from extensions import db
from models.interview import Interview
from models.interview_question import InterviewQuestion
from models.interview_evaluation import InterviewEvaluation
from models.user import User
from models.job_requirement import JobRequirement
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_


class InterviewService:

    @staticmethod
    def create_interview(data):
        """创建面试"""
        try:
            interview = Interview(
                title=data.get("title"),
                description=data.get("description"),
                job_requirement_id=data.get("job_requirement_id"),
                interviewer_id=data.get("interviewer_id"),
                interviewee_id=data.get("interviewee_id"),
                question_count=data.get("question_count", 5),
                status="draft",
            )
            db.session.add(interview)
            db.session.commit()
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_interviews_by_interviewer(interviewer_id, status=None):
        """获取面试官的面试列表"""
        try:
            query = Interview.query.filter_by(interviewer_id=interviewer_id)
            if status:
                query = query.filter_by(status=status)
            interviews = query.order_by(Interview.created_at.desc()).all()
            return [interview.to_dict() for interview in interviews], None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def get_interviews_by_interviewee(interviewee_id, status=None):
        """获取面试者的面试列表（只返回已分配及之后状态的面试）"""
        try:
            query = Interview.query.filter_by(interviewee_id=interviewee_id)

            # 面试者只能看到非草稿状态的面试
            query = query.filter(Interview.status != "draft")

            if status:
                query = query.filter_by(status=status)
            interviews = query.order_by(Interview.created_at.desc()).all()
            return [interview.to_dict() for interview in interviews], None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def get_interview_by_id(interview_id):
        """根据ID获取面试详情"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def update_interview(interview_id, data):
        """更新面试信息"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 更新字段
            if "title" in data:
                interview.title = data["title"]
            if "description" in data:
                interview.description = data["description"]
            if "job_requirement_id" in data:
                interview.job_requirement_id = data["job_requirement_id"]
            if "interviewee_id" in data:
                interview.interviewee_id = data["interviewee_id"]
            if "question_count" in data:
                interview.question_count = data["question_count"]
            if "status" in data:
                interview.status = data["status"]

            interview.updated_at = datetime.utcnow()
            db.session.commit()
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_interview(interview_id):
        """删除面试"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return False, "面试不存在"

            # 删除相关的题目和评价
            InterviewQuestion.query.filter_by(interview_id=interview_id).delete()
            InterviewEvaluation.query.filter_by(interview_id=interview_id).delete()

            db.session.delete(interview)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def assign_interview(interview_id, interviewee_id):
        """分配面试给面试者"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 检查面试者是否存在
            interviewee = User.query.filter_by(
                id=interviewee_id, role="interviewee"
            ).first()
            if not interviewee:
                return None, "面试者不存在"

            interview.interviewee_id = interviewee_id
            interview.status = "assigned"
            interview.updated_at = datetime.utcnow()

            db.session.commit()
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def start_interview(interview_id):
        """开始面试"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            if interview.status != "assigned":
                return None, "面试状态不正确"

            interview.status = "in_progress"
            interview.started_at = datetime.utcnow()
            interview.updated_at = datetime.utcnow()

            db.session.commit()
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def complete_interview(interview_id):
        """完成面试"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            if interview.status != "in_progress":
                return None, "面试状态不正确"

            interview.status = "completed"
            interview.completed_at = datetime.utcnow()
            interview.updated_at = datetime.utcnow()

            db.session.commit()
            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    # 题目管理相关方法
    @staticmethod
    def add_question(interview_id, question_data):
        """为面试添加题目"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 获取当前最大的order_index
            max_order = (
                db.session.query(db.func.max(InterviewQuestion.order_index))
                .filter_by(interview_id=interview_id)
                .scalar()
                or 0
            )

            question = InterviewQuestion(
                interview_id=interview_id,
                question_text=question_data.get("question_text"),
                question_type=question_data.get("question_type", "text"),
                options=question_data.get("options"),
                reference_answer=question_data.get("reference_answer"),
                score=question_data.get("score", 10),
                order_index=max_order + 1,
            )

            db.session.add(question)
            db.session.commit()
            return question.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_interview_questions(interview_id, for_candidate=False):
        """获取面试题目"""
        try:
            questions = (
                InterviewQuestion.query.filter_by(interview_id=interview_id)
                .order_by(InterviewQuestion.order_index)
                .all()
            )

            if for_candidate:
                return [question.to_candidate_dict() for question in questions], None
            else:
                return [question.to_dict() for question in questions], None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def update_question(question_id, question_data):
        """更新题目"""
        try:
            question = InterviewQuestion.query.get(question_id)
            if not question:
                return None, "题目不存在"

            # 更新字段
            if "question_text" in question_data:
                question.question_text = question_data["question_text"]
            if "question_type" in question_data:
                question.question_type = question_data["question_type"]
            if "options" in question_data:
                question.options = question_data["options"]
            if "reference_answer" in question_data:
                question.reference_answer = question_data["reference_answer"]
            if "score" in question_data:
                question.score = question_data["score"]
            if "order_index" in question_data:
                question.order_index = question_data["order_index"]

            question.updated_at = datetime.utcnow()
            db.session.commit()
            return question.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_question(question_id):
        """删除题目"""
        try:
            question = InterviewQuestion.query.get(question_id)
            if not question:
                return False, "题目不存在"

            db.session.delete(question)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def submit_answer(question_id, answer):
        """提交答案"""
        try:
            question = InterviewQuestion.query.get(question_id)
            if not question:
                return None, "题目不存在"

            question.candidate_answer = answer
            question.updated_at = datetime.utcnow()

            db.session.commit()
            return question.to_candidate_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    # 评价相关方法
    @staticmethod
    def create_evaluation(interview_id, evaluator_id, evaluation_data):
        """创建面试评价"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            if interview.status != "pending_evaluation":
                return None, "面试尚未进入待评价状态"

            # 检查是否已有评价
            existing_evaluation = InterviewEvaluation.query.filter_by(
                interview_id=interview_id
            ).first()
            if existing_evaluation:
                return None, "该面试已有评价"

            evaluation = InterviewEvaluation(
                interview_id=interview_id,
                evaluator_id=evaluator_id,
                total_score=evaluation_data.get("total_score", 0),
                max_score=evaluation_data.get("max_score", 100),
                overall_comments=evaluation_data.get("overall_comments"),
                skill_ratings=evaluation_data.get("skill_ratings"),
                recommendations=evaluation_data.get("recommendations"),
                is_passed=evaluation_data.get("is_passed", False),
                decision_reason=evaluation_data.get("decision_reason"),
            )

            db.session.add(evaluation)

            # 根据是否完成评价来决定是否更新面试状态
            complete_evaluation = evaluation_data.get("complete_evaluation", False)
            if complete_evaluation:
                interview.status = "completed"
                evaluation.is_finalized = True  # 标记评价已完成
                interview.updated_at = datetime.utcnow()

            db.session.commit()
            return evaluation.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_evaluation(interview_id):
        """获取面试评价"""
        try:
            evaluation = InterviewEvaluation.query.filter_by(
                interview_id=interview_id
            ).first()
            if not evaluation:
                return None, "评价不存在"
            return evaluation.to_dict(), None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def update_evaluation(evaluation_id, evaluation_data):
        """更新面试评价"""
        try:
            evaluation = InterviewEvaluation.query.get(evaluation_id)
            if not evaluation:
                return None, "评价不存在"

            # 检查评价是否已完成（已锁定）
            if hasattr(evaluation, "is_finalized") and evaluation.is_finalized:
                return None, "评价已完成，不能再修改"

            # 更新字段
            if "total_score" in evaluation_data:
                evaluation.total_score = evaluation_data["total_score"]
            if "max_score" in evaluation_data:
                evaluation.max_score = evaluation_data["max_score"]
            if "overall_comments" in evaluation_data:
                evaluation.overall_comments = evaluation_data["overall_comments"]
            if "skill_ratings" in evaluation_data:
                evaluation.skill_ratings = evaluation_data["skill_ratings"]
            if "recommendations" in evaluation_data:
                evaluation.recommendations = evaluation_data["recommendations"]
            if "is_passed" in evaluation_data:
                evaluation.is_passed = evaluation_data["is_passed"]
            if "decision_reason" in evaluation_data:
                evaluation.decision_reason = evaluation_data["decision_reason"]

            evaluation.updated_at = datetime.utcnow()

            # 检查是否要完成评价
            complete_evaluation = evaluation_data.get("complete_evaluation", False)
            if complete_evaluation:
                evaluation.is_finalized = True
                # 更新面试状态为已完成
                interview = Interview.query.get(evaluation.interview_id)
                if interview:
                    interview.status = "completed"
                    interview.updated_at = datetime.utcnow()

            db.session.commit()
            return evaluation.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def score_question(question_id, score, comments):
        """为题目评分"""
        try:
            question = InterviewQuestion.query.get(question_id)
            if not question:
                return None, "题目不存在"

            question.actual_score = score
            question.comments = comments
            question.updated_at = datetime.utcnow()

            db.session.commit()
            return question.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def complete_interview(interview_id, interviewee_id):
        """完成面试（面试者调用）"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 检查权限
            if interview.interviewee_id != interviewee_id:
                return None, "无权限完成此面试"

            # 检查面试状态
            if interview.status == "completed":
                return None, "面试已完成"

            if interview.status != "assigned" and interview.status != "in_progress":
                return None, "面试状态不正确，无法完成"

            # 检查是否所有题目都已回答
            questions = InterviewQuestion.query.filter_by(
                interview_id=interview_id
            ).all()
            unanswered_questions = [
                q
                for q in questions
                if not q.candidate_answer or not q.candidate_answer.strip()
            ]

            if unanswered_questions:
                return (
                    None,
                    f"还有 {len(unanswered_questions)} 道题目未回答，请完成所有题目后再提交",
                )

            # 更新面试状态 - 改为待评价状态
            interview.status = "pending_evaluation"
            interview.completed_at = datetime.utcnow()

            # 如果没有开始时间，设置开始时间（兼容旧数据）
            if not interview.started_at:
                interview.started_at = interview.created_at

            interview.updated_at = datetime.utcnow()
            db.session.commit()

            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def start_interview(interview_id, interviewee_id):
        """开始面试（面试者调用）"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 检查权限
            if interview.interviewee_id != interviewee_id:
                return None, "无权限开始此面试"

            # 检查面试状态
            if interview.status == "completed":
                return None, "面试已完成"

            if interview.status != "assigned":
                return None, "面试状态不正确，无法开始"

            # 更新面试状态
            interview.status = "in_progress"
            interview.started_at = datetime.utcnow()
            interview.updated_at = datetime.utcnow()
            db.session.commit()

            return interview.to_dict(), None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_interview_status(interview_id, new_status, current_user_id):
        """更新面试状态"""
        try:
            interview = Interview.query.get(interview_id)
            if not interview:
                return None, "面试不存在"

            # 检查权限：只有面试官才能更新状态
            if interview.interviewer_id != current_user_id:
                return None, "无权限更新此面试状态"

            # 状态转换规则检查
            current_status = interview.status

            # 从草稿到已分配的规则
            if current_status == "draft" and new_status == "assigned":
                if not interview.interviewee_id:
                    return None, "面试必须先分配给面试者才能派发"

            # 其他状态转换规则可以在这里添加
            elif current_status == "assigned" and new_status == "draft":
                return None, "已分配的面试不能回到草稿状态"
            elif (
                current_status in ["completed", "evaluated"]
                and new_status != current_status
            ):
                return None, f"已{current_status}的面试状态不能更改"

            # 更新状态和时间
            interview.status = new_status
            interview.updated_at = datetime.utcnow()

            # 如果状态变为已分配，记录分配时间
            if new_status == "assigned":
                interview.assigned_at = datetime.utcnow()

            db.session.commit()
            return interview.to_dict(), None

        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)
