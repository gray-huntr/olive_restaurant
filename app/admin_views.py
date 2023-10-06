from app import app
from flask import render_template, request, flash, redirect
import pymysql
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])


@app.route("/menu_upload", methods=['POST', 'GET'])
def menu_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', "warning")
            return redirect("/menu_upload")
        file = request.files['file']
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'warning')
            return redirect('/menu_upload')
        # If all checks are passed, the app proceeds to submit the file

        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sql = ("insert into menu(name,picture,description,price,category) "
                   "values(%s,%s,%s,%s,%s)")
            try:
                #  connect to database
                conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                                       password=app.config["DB_PASSWORD"],
                                       database=app.config["DB_NAME"])
                cursor = conn.cursor()
                # send to database
                cursor.execute(sql, (name, filename, description, price, category))
                # Save to database
                conn.commit()
                flash("Uploaded Successfully", "success")
                return redirect('/menu_upload')
                # if error occurs, display error message
            except:
                flash("Upload Failed", "danger")
                return redirect('/menu_upload')
        # If file is not on allowed list, display error message
        else:
            flash("Uploaded File Not Allowed", "warning")
            return redirect('/menu_upload')
    else:
        return render_template('admin/menu_upload.html')
