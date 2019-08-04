from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
import h2o, os
import pandas as pd


print(os.listdir())
app = Flask(__name__)
h2o.init()

Bootstrap(app)
B = h2o.load_model(
    "C:\\Users\\Maria\\Desktop\\creditscore_mbugua\\load_model\\good\\GBM_model_python_1564914397585_628"
)

loans = pd.read_csv("loans.csv")


def trump(x, df):
    if x * 100 < 21:
        return pd.DataFrame(columns =['BANKS', 'LOANS', 'RATES', 'MAX_AMOUNT'])
    elif x * 100 < 30:
        fil = df.RATES > 14
        fil1 = df.RATES < 20
        return df[fil & fil1]
    elif x * 100 < 40:
        fil = df.RATES >= 10
        fil1 = df.RATES < 14
        return df[fil & fil1]
    elif x * 100 < 50:
        fil = df.RATES > 5
        fil1 = df.RATES < 10
        return df[fil & fil1]
    else:
        filters = df.RATES < 5
        return df[filters]


# print(B)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # get form data
        loan_amnt = int(request.form.get("loanamount"))
        funded_amnt = int(request.form.get("funded"))
        installment = int(request.form.get("installment"))
        int_rate = float(request.form.get("interest"))
        term = int(request.form.get("term"))
        emp_length = int(request.form.get("employment"))
        home_ownership = request.form.get("home")
        annual_inc = int(request.form.get("income"))
        purpose = request.form.get("purpose")
        kamau = [
            loan_amnt,
            funded_amnt,
            installment,
            int_rate,
            term,
            emp_length,
            home_ownership,
            annual_inc,
            purpose,
        ]

        C = pd.DataFrame(
            [kamau],
            columns=[
                "loan_amnt",
                "funded_amnt",
                "installment",
                "int_rate",
                "term",
                "emp_length",
                "home_ownership",
                "annual_inc",
                "purpose",
            ],
        )
        C = h2o.H2OFrame(C)
        print(C)
        V = B.predict(C)
        good = V[0, 1]  # probability of being good
        melania = trump(good, loans)
        print(melania)
        banks =[i for i in melania.BANKS[:2]]
        loa =[i for i in melania.LOANS[:2]]
        interest =[i for i in melania.RATES[:2]]
        maxi =[i for i in melania.MAX_AMOUNT[:2]]
        return render_template( "result.html", v=V[0, 0], proba=good,bank =banks,loan =loa,ints =interest,maxi =maxi)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
