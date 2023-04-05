from flask import Flask, render_template, request, redirect, send_from_directory
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import pymysql
import pymysql.cursors

login_manager = LoginManager()



app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'something_random'


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
    cursor = connection.cursor()

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


@app.route("/feed")
@login_required
def post():
    cursor=connection.cursor()

    cursor.execute("SELECT * FROM `Posts` JOIN `Users` ON `Posts`.`user_id` = `Users`.`id` ORDER BY `date` DESC;")

    results = cursor.fetchall()

    return render_template("post.html.jinja", posts = results)


@app.route("/sign-in", methods=['POST', 'GET'])
def sign_in():
    if current_user.is_authenticated:
        return redirect('/feed')
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM `Users` WHERE `username` = '{request.form['username']}' ")
        result = cursor.fetchone()

        if result is None:
            return render_template("sign-in.html.jinja")

        if request.form['password'] == result['password']:
            user = User(result['id'], result['username'], result['banned'])

            login_user(user)

            return redirect('/feed')
        else:
            return render_template("sign_in.html.jinja")



        return request.form
    
    elif request.method == 'GET':
        return render_template("sign_in.html.jinja")
    



@app.route('/sign-out')
def sign_out():
    logout_user()

    return redirect('/sign-in')



@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect('/feed')
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

        return redirect('/sign-in')



        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")


@app.route('/post', methods=['POST'])
@login_required
def create_post():
    cursor = connection.cursor()
    profile = request.files['file']
    file_name = profile.filename
    file_extension = file_name.split('.')[-1]

    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        profile.save('media/posts/' + file_name)
    else:
        raise Exception('invalid file type')
    
    user_id = current_user.id

    cursor.execute("""INSERT INTO `Posts` (`post_image`, `post_feed`, `user_id`) VALUES(%s, %s, %s)""", (file_name, request.form['text'], user_id))
    return redirect('/feed')


@app.get('/media/<path:path>')
def send_media(path):
    return send_from_directory('media', path)



if __name__ == '__main__':
    app.run(debug=True)
