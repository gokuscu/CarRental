import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://ltnk:pass@localhost/car_rental_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
