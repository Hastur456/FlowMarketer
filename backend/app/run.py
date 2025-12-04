if __name__ == "__main__":
    import subprocess
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])