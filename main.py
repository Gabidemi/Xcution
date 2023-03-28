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


if __name__ == '__main__':
    app.run(debug=True)