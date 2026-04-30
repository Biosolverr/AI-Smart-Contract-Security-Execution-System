import os

def deploy():

    print("Building product...")

    os.system("pip install fastapi uvicorn")

    print("Starting server...")

    os.system("python product/main.py")


if __name__ == "__main__":
    deploy()
