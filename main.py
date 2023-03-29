from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors

app = Flask(__name__)

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
        cursor.execute("""
            INSERT INTO `users` (`username`, `password`, `email`, `date-of-birth`, `photo`, `display-name`, `phone-number`, )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        
        """, [request])



        return request.form
    elif request.method == 'GET':
        return render_template("sign_up.html.jinja")


if __name__ == '__main__':
    app.run(debug=True)
