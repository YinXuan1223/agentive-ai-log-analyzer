
from flask import Flask
from flask_cors import CORS
from my_routes.api import api_blueprint
# from dotenv import load_dotenv

# load_dotenv()
app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
