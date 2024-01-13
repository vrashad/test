from sqlalchemy import text
from app import app, db, Cat


def initialize_database():
    with app.app_context():
        db.create_all()

        if not db.session.query(Cat).first():
            with open('init.sql', 'r') as file:
                sql_script = file.read()

            sql = text(sql_script)
            db.session.execute(sql)
            db.session.commit()

if __name__ == "__main__":
    initialize_database()
