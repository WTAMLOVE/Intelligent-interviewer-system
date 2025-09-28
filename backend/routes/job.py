from flask import request
from flask_restx import Namespace, Resource, fields
from services.job_service import create_job, get_job, list_jobs, update_job, delete_job
from flask_jwt_extended import jwt_required
from utils.roles import roles_required

ns = Namespace("jobs", description="岗位管理")

job_model = ns.model(
    "Job",
    {
        "id": fields.Integer(description="岗位ID"),
        "job_title": fields.String(required=True),
        "description": fields.String(required=False),
        "skills": fields.List(fields.String, required=False),
        "created_at": fields.String(description="创建时间"),
    },
)


@ns.route("/")
class JobList(Resource):
    @ns.marshal_list_with(job_model)
    def get(self):
        return list_jobs()

    @ns.expect(job_model)
    @jwt_required()  # 临时改为只需要登录，不限制角色
    def post(self):
        data = request.json
        job = create_job(data)
        return job.to_dict(), 201


@ns.route("/<int:job_id>")
class JobItem(Resource):
    def get(self, job_id):
        job = get_job(job_id)
        if not job:
            ns.abort(404)
        return job.to_dict()

    @ns.expect(job_model)
    @jwt_required()  # 临时改为只需要登录，不限制角色
    def put(self, job_id):
        data = request.json
        job = update_job(job_id, data)
        if not job:
            ns.abort(404)
        return job.to_dict()

    @jwt_required()  # 临时改为只需要登录，不限制角色
    def delete(self, job_id):
        delete_job(job_id)
        return {"message": "deleted"}
