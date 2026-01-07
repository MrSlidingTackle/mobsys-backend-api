from flask import Flask, jsonify
import backend.classes.aiven as aiven
from sqlalchemy import select
from backend.routes.products import init_routes

app = Flask(__name__)

# Initialize database connection
aiven_env = aiven.AivenEnvironment()
db = aiven.AivenDatabase(aiven_env)
db.connect()

# Register blueprints
products_blueprint = init_routes(db)
app.register_blueprint(products_blueprint)


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to mobsys-backend-api",
        "version": "0.1.0",
        "endpoints": {
            "/": "Home",
            "/health": "Health check",
            "/api/products": "Get all products",
            "/api/products/<id>": "Get product by ID"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with db.session as session:
            session.execute(select(1))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
