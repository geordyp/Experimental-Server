from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<string:task_category>", methods=['GET', 'POST'])
def main(task_category):
    return render_template('home.html',
                           name=task_category)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
