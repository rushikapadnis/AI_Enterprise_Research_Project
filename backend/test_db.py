from sqlalchemy import text

from app.db.database import engine


with engine.begin() as connection:
    connection.execute(
        text(
            """
            INSERT INTO users (email)
            VALUES (:email)
            """
        ),
        {
            "email": "aman@example.com"
        }
    )

print("User inserted successfully")