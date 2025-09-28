# 智能面试官 (示例项目)
学习如何使用`Github Copilot`进行`Vibe Coding`

后端 (Flask):

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export FLASK_APP=manage.py
flask run

前端 (Vite + Vue3):

cd frontend
npm install
npm run dev
