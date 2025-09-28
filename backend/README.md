# 智能面试官 - 后端 (Flask)

快速启动:

1. 创建并激活虚拟环境
2. pip install -r requirements.txt
3. 设置环境变量或复制 `.env.example` 到 `.env`
4. 初始化数据库迁移示例:

```bash
export FLASK_APP=manage.py
flask db init
flask db migrate -m "init"
flask db upgrade
```

5. 运行: `flask run`
