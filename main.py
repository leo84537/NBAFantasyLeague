from fastapi import FastAPI
from routes import players, teams

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)


@app.get("/")
def root():
    return {"WELCOME TO THE INEVITABILITY"}