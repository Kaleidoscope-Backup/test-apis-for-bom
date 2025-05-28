from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/run_code")
async def run_code(request: Request):
    user_input = request.query_params.get("code")
    result = eval(user_input)  # 🔥 CRITICAL: RCE vulnerability
    return {"result": result}
