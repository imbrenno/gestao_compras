from flask import render_template, jsonify, Blueprint, make_response, redirect, session

bp = Blueprint(
    "index",
    __name__,
    template_folder="templates",
)


class IndexCtrl:
    @bp.route("/")
    def inicial_template():
        print(session)
        if session:
            return render_template("index.html")

        else:
            return redirect("/login")
