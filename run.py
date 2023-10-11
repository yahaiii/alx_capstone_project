from flask import Flask
from app.routes.landing import landing_blueprint

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

# Register the landing page Blueprint
app.register_blueprint(landing_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
