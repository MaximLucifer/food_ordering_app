from app import create_app
from schema import create_tables

app = create_app()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)