class Config(object):
    Debug = False

    SECRET_KEY = "dKH,(}D%kcC0*@L"
    # Details of the database
    DB_HOST = "localhost"
    DB_USERNAME = "root"
    DB_PASSWORD = ""
    DB_NAME = "olive_garden"

    # Details of file uploads
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    UPLOAD_FOLDER = 'app/static/images/'
