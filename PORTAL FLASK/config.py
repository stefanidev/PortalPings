import os

SECRET_KEY = 'vivo@123'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '',
        servidor = '127.0.0.1',
        database = 'portalpings'
    )

"""UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'"""