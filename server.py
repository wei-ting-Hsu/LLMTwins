import json
# import sqlite3
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from database import initDB, selectFromDB, saveProfileToDB, \
    saveAPITableToDB, deleteFromDB, listFromDB
from models import regUser, getUser, prompt
from LLM.LLMTwins import DigitalTwins

# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# Instances of digital twins are stored in this dictionary
dt_instances = {}

# Initialize database
conn, cursor = initDB()

# Health Check
@app.get("/health")
async def health():
    return {"result": "Healthy Server!"}

@app.post("/register_llm_twins")
async def register_llm_twins(user: regUser):
    # Check if user is already registered
    result = selectFromDB(conn, "llm_twins", "name", user.name)

    if result is not None:
        # Return 404 response
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is already registered")

    dt = DigitalTwins()
    result, profile, api_table = dt.register_llm_twins(user.name, user.description)

    if (result):
        profile["名稱"] = user.name
        dt_instances[profile["名稱"]] = profile
    else:
        # Return 404 response
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    # Save profile to database
    result = saveProfileToDB(conn, user)

    # Save API table
    if (result == True):
        result = saveAPITableToDB(conn, user, api_table)

    # Return Profile & API Table
    return {"profile": profile, "api_table": api_table}

# Get LLM Digital Twins with User ID
@app.post("/get_llm_twins")
async def get_llm_twins(user: getUser):
    result = selectFromDB(conn, "llm_twins", "name", user.name)

    # Check if result is None
    if result is None:
        # Return 404 response
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    # TODO
    # Document loader
    # Agent
    # RAG

    return {"result": result}

# Get Digital Twins API table
@app.post("/get_llm_twins_api")
async def get_llm_twins_api(user: getUser):
    result = selectFromDB(conn, "llm_twins_api", "name", user.name)

    # Check if result is None
    if result is None:
        # Return 404 response
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    return {"result": json.loads(result[1])}

# Delete LLM Digital Twins with User ID
@app.post("/delete_llm_twins")
async def delete_llm_twins(user: getUser):
    result = deleteFromDB(conn, "llm_twins", "name", user.name)

    # Check if result is False
    if result == False:
        # Return 404 response
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    # TODO: Delete from dt_instances
    return {"message": "Digital Twin for this user has been deleted"}

# List all LLM Digital Twins
@app.get("/list_llm_twins")
async def list_llm_twins():
    result = listFromDB(conn, "llm_twins")

    return {"result": result}

# Intent recognition
@app.post("/intent_recognition")
async def intent_recognition(prompt: prompt):
    result = False

    # Get user from database
    profile = selectFromDB(conn, "llm_twins", "name", prompt.role)

    if profile is None:
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    # Get intent from database
    api_table = selectFromDB(conn, "llm_twins_api", "name", prompt.role)

    if api_table is None:
        raise HTTPException(status_code = 404, detail = "API table for this user is not registered")

    dt = DigitalTwins()
    result, message = dt.intent_recognition(prompt.message)

    return {"result": result, "message": message}

@app.post("/prompt_llm_twins")
async def prompt_llm_twins(prompt: prompt):
    # Get user from database
    profile = selectFromDB(conn, "llm_twins", "name", prompt.role)

    if profile is None:
        raise HTTPException(status_code = 404, detail = "Digital Twin for this user is not registered")

    # Get intent from database
    api_table = selectFromDB(conn, "llm_twins_api", "name", prompt.role)

    if api_table is None:
        raise HTTPException(status_code = 404, detail = "API table for this user is not registered")

    dt = DigitalTwins()
    result = dt.prompt_llm_twins(prompt.role, profile[1] ,prompt.message, api_table)

    return {"result": result}