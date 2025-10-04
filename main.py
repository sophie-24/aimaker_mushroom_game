from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MUSHROOM_DATA = [
    {'file': f'{i}.png', 'poisonous': (i % 2 != 0)} for i in range(1, 11)
]

@app.get("/api/mushrooms", response_class=JSONResponse)
async def get_mushrooms():
    """전체 버섯 데이터 목록을 JSON으로 반환하는 API 엔드포인트"""
    return MUSHROOM_DATA

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "mushrooms": MUSHROOM_DATA})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request):
    """퀴즈 페이지를 렌더링합니다. 문제 데이터는 페이지의 JavaScript가 /api/mushrooms를 통해 가져옵니다."""
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.post("/check", response_class=JSONResponse)
async def check(request: Request, image_file: str = Form(...), user_answer: str = Form(...)):
    mushroom = next((m for m in MUSHROOM_DATA if m['file'] == image_file), None)
    
    if not mushroom:
        return JSONResponse(status_code=404, content={"is_correct": False, "message": "오류 발생"})

    correct_answer = "독버섯" if mushroom['poisonous'] else "식용버섯"
    is_correct = user_answer == correct_answer
    
    if is_correct:
        message = "<h3>✅ 정답입니다! 방금의 학습으로 AI가 더 똑똑해졌습니다. 올바른 데이터를 가르쳐주셔서 고맙습니다.</h3>"
    else:
        message = f"<h3>❌ 오답! 이 버섯은 '{correct_answer}'입니다. AI가 혼란스러워합니다.</h3>"
    
    return JSONResponse(content={"is_correct": is_correct, "message": message})