import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SUPABASE_URL"] = os.getenv("SUPABASE_URL")

    app.config["SUPABASE_ANON_KEY"] = os.getenv(
        "SUPABASE_ANON_KEY"
    )


    from app.routes.auth import auth_bp
    from app.routes.main import main
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    

    return app