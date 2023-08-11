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
            user_data = data["user"]
            statement_user = select(Users).where(Users.user == user_data)
            usuario: Users = Database().get_one(statement_user)
            password_db = usuario.password
            user_active = usuario.active

            if user_active == True:
                print("checkd user")
                session["user"] = data["user"]

                if validate_password(data["password"], password_db):
                    print("Checked Password")
                    return redirect("/")

                else:
                    return redirect("/login")

            else:
                return redirect("/login")

        except Exception as e:
            print(e)
            return redirect("/login")

    @bp.route("/logout")
    def sigout():
        session.pop("user", None)
        print(session)
        return redirect("/login")
