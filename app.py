from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
import h2o, os
import pandas as pd


print(os.listdir())
app = Flask(__name__)
h2o.init()

Bootstrap(app)
B = h2o.load_model("C:\\test\\j\\DRF_model_python_1564849389326_368")

# print(B)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # get form data
        age = request.form.get("age")
        height = request.form.get("height")
        print({"Age": age, "Height": height})
        t = h2o.H2OFrame(pd.DataFrame([[age, height]], columns=["d1", "d2"]))
        V = B.predict(t)
        print(V[0, 0])
        return render_template("result.html", v=V[0, 0])

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5500)
