from flask import Flask
from routes.entity_routes import entity_bp
from routes.record_routes import record_bp

app = Flask(__name__)

app.register_blueprint(entity_bp)
app.register_blueprint(record_bp)

if __name__ == "__main__":
    app.run(debug=True)