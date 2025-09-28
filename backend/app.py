from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS
from config import Config
from extensions import db, jwt
import logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    # initialize migrate via extensions so CLI commands are registered on import
    from extensions import migrate

    migrate.init_app(app, db)

    # JWT错误处理器
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "登录已过期，请重新登录"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return {"message": "无效的登录凭证"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return {"message": "需要登录才能访问"}, 401

    # 通用错误处理器
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return {"message": "服务器内部错误"}, 500

    api = Api(
        app, version="1.0", title="智能面试官 API", description="基础 RESTful API"
    )

    # import and register namespaces
    from routes.auth import ns as auth_ns
    from routes.job import ns as job_ns
    from routes.interview import ns as interview_ns
    from routes.resume import ns as resume_ns
    from routes.user import ns as user_ns

    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(job_ns, path="/api/jobs")
    api.add_namespace(interview_ns, path="/api/interviews")
    api.add_namespace(resume_ns, path="/api/resumes")
    api.add_namespace(user_ns, path="/api/users")

    # Ensure a super-admin user exists (configured via env vars or .env fallback)
    import os
    from os import path
    from dotenv import dotenv_values
    from services.user_service import create_user as public_create_user
    from models.user import User

    # try environment variables first
    super_username = os.environ.get("SUPER_ADMIN_USERNAME")
    super_email = os.environ.get("SUPER_ADMIN_EMAIL")
    super_password = os.environ.get("SUPER_ADMIN_PASSWORD")

    # If any are missing, try reading from backend/.env directly (keys unchanged)
    if not (super_username and super_email and super_password):
        basedir = path.abspath(path.dirname(__file__))
        env_path = path.join(basedir, ".env")
        try:
            values = dotenv_values(env_path)
        except Exception:
            values = {}

        super_username = super_username or values.get("SUPER_ADMIN_USERNAME")
        super_email = super_email or values.get("SUPER_ADMIN_EMAIL")
        super_password = super_password or values.get("SUPER_ADMIN_PASSWORD")

    if super_username and super_email and super_password:
        with app.app_context():
            existing = User.query.filter_by(role="admin").first()
            if not existing:
                # Create admin user directly bypassing public restriction
                from utils.security import hash_password

                pw_hash = hash_password(super_password)
                admin = User(
                    username=super_username,
                    email=super_email,
                    password_hash=pw_hash,
                    role="admin",
                )
                db.session.add(admin)
                db.session.commit()
                app.logger.info("Super admin created: %s", super_username)
            else:
                app.logger.info("Super admin already exists: %s", existing.username)
    else:
        app.logger.info(
            "Super admin credentials not found in env or .env; skipping creation"
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
