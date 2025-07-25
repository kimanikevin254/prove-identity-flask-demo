import os
from flask_cors import CORS
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)