import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'financijsko_pracenje.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'tajni_ključ'

