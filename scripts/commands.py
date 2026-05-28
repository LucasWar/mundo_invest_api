import os

def dev():
    os.system("docker compose up db -d")
    os.system("uvicorn app.main:app --reload")

def test():
    os.system("pytest")

def build():
    os.system("docker compose up -d")
