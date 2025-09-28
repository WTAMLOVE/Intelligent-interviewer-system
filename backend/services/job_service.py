from extensions import db
from models.job_requirement import JobRequirement


def create_job(data):
    job = JobRequirement(
        job_title=data.get("job_title"),
        description=data.get("description"),
        skills=data.get("skills") or [],
    )
    db.session.add(job)
    db.session.commit()
    return job


def get_job(jid):
    return JobRequirement.query.get(jid)


def list_jobs():
    return JobRequirement.query.order_by(JobRequirement.created_at.desc()).all()


def update_job(jid, data):
    job = JobRequirement.query.get(jid)
    if not job:
        return None
    job.job_title = data.get("job_title", job.job_title)
    job.description = data.get("description", job.description)
    job.skills = data.get("skills", job.skills)
    db.session.commit()
    return job


def delete_job(jid):
    job = JobRequirement.query.get(jid)
    if job:
        db.session.delete(job)
        db.session.commit()
