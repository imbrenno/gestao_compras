from main.database.models.database import Database, select
from flask import (
    abort,
    Blueprint,
    make_response,
    session,
    redirect,
    render_template,
    request,
)
from main.database.models.users_model import Users
from main.utils.utils import validate_password


bp = Blueprint(
    "login",
    __name__,
    template_folder="templates",
)


class LoginController:
    @bp.route("/login", methods=["POST", "GET"])
    def sigin():
        if request.method == "GET":
            return render_template("login.html", titulo="Faça Login")

        try:
            data = request.form
            statement_user = select(Users).where(Users.user == data["user"])
            usuario: Users = Database().get_one(statement_user)
            print("Checking user")
            if usuario.active:
                print("Checking user: Active user")
                session["user"] = data["user"]

                if validate_password(data["password"], usuario.password):
                    print("Checked Password")
                    return redirect("/")
                print("Checking user: Username or password is invalid")
                return redirect("/login")
            print("Checking user: Disabled user")
            return redirect("/login")

        except Exception as e:
            print(e)
            return redirect("/login")

    @bp.route("/logout")
    def signout():
        session.pop("user", None)
        return redirect("/login")
