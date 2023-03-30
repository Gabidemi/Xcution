from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
import pymysql
import pymysql.cursors

login_manager = LoginManager()



app = Flask(__name__)
login_manager.init_app(app)


class User:
    def __init__(self, id, username, banned):
        self.is_authenticated = True
        self.is_anonymous = False
        self.is_active = not banned

        self.username = username
        self.id = id


    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def user_loader(user_id):
    cursor = connection.cursor

    cursor.execute("SELECT * FROM `Users` WHERE `id` = " + user_id)

    result = cursor.fetchone()

    if result is None:
        return None
    
    return User(result['id'], result['username'], result['banned'])


@app.route("/")
def index():
    print("Xcution_Testing_Site")
    return render_template("home.html.jinja")




connection = pymysql.connect(
    host="10.100.33.60",
    user="gabidemi",
    password="244655536",
    database="gabidemi_Social",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


@app.route("/post")
def post():
    cursor=connection.cursor()

    cursor.execute("SELECT * FROM `Posts` JOIN `Users` ON `Posts`.`user_id` = `Users`.`id` ORDER BY `date` DESC;")

    results = cursor.fetchall()

    return render_template("post.html.jinja", posts = results)


@app.route("/sign-in")
def sign_in():
    return render_template("sign_in.html.jinja")
@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        #handle signup
        cursor = connection.cursor()

        profile = request.files['picture']
        file_name = profile.filename
        file_extension = file_name.split('.')[-1]

        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            profile.save('media/users/' + file_name)
        else:
            raise Exception('invalid file type')




        cursor.execute("""
            INSERT INTO `Users` (`username`, `password`, `email`, `date_of_birth`, `photo`, `display_name`, `phone_number` )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        
        """, (request.form['username'], request.form['password'], request.form['email'], request.form['date'], file_name, request.form['display'], request.form['phone-number']))

        return redirect('/post')



        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")


if __name__ == '__main__':
    app.run(debug=True)
