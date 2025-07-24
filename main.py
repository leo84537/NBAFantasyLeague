from fastapi import FastAPI
from routes.players import router as playersrouter
from routes.teams import router as teamsrouter
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start_scheduler
app = FastAPI()

app.include_router(playersrouter)
app.include_router(teamsrouter)

# http://localhost:5173
app.add_middleware(
  CORSMiddleware,
  allow_origins=["https://nba-fantasy-league-hurh9hdfu-leo-suns-projects.vercel.app", "http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["*"],
)

# Updates to newest game played
# start_scheduler()

@app.get("/")
def root():
    return {"WELCOME TO THE INEVITABILITY"}