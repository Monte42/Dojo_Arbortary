from belt_app import app
from belt_app.controllers import users, trees, visitors

if __name__ == "__main__":
    app.run(debug=True)