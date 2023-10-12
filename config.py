# config.py

# Flask Configuration
SECRET_KEY = '4dLove_of_Br3Ad'
DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/Breadcrumbs'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yahayaal:password@db4free.net/breadcrumbs'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Set to False to improve performance

# Flask-Mail Configuration (if using email functionality)
# MAIL_SERVER = 'smtp.example.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'your_email@example.com'
# MAIL_PASSWORD = 'your_email_password'

# Other Application Configuration
# ...

