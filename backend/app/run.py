from app.config import settings
import subprocess


if __name__ == "__main__":
    subprocess.run(["uvicorn", "app.main:app", "--host", f"{settings.run.app_host}", "--port", f"{settings.run.app_port}"])
