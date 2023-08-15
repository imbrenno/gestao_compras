from main.database.models.database import Database, select
import json
from flask import (
    jsonify,
    Blueprint,
    abort,
    request,
    make_response,
    redirect,
    render_template,
    session,
)
from main.database.models.users_model import Users
from main.utils.enums.users import GenderEnum
from main.utils.utils import hash_password

bp = Blueprint(
    "users",
    __name__,
    template_folder="templates",
)


class UsuarioCtrl:
    @staticmethod
    @bp.route("/create-user", methods=["POST", "GET"])
    def create_user():
        if session:
            if request.method == "GET":
                return render_template("create_user.html", titulo="Novo Usuário")

            try:
                data = request.form
                password = hash_password(data["password"])
                user = UsuarioCtrl.check_user_exist(data["user"])
                if user is False:
                    if data:
                        usuario = Users(
                            user=data["user"],
                            password=password,
                            fullName=data["fullName"],
                            document=data["document"],
                            gender=data["gender"],
                        )
                        Database().save(usuario)

                    return redirect("/list-users")

                else:
                    return make_response(
                        jsonify({"menssage": "Usuario ja existe"}), 409
                    )

            except Exception as e:
                print(e)
                return abort(400)

        return redirect("/login")

    @bp.route("/list-users")
    def users_all():
        if session:
            statement = select(Users)
            users = Database().get_all(statement)
            users_json = []
            for user in users:
                users_json.append(
                    {
                        "id": user.id,
                        "user": user.user,
                        "userGroupId": user.userGroupId,
                        "fullName": user.fullName,
                        "document": user.document,
                        "active": user.active,
                        "userGroupId": user.userGroupId,
                    }
                )
            return render_template(
                "list_users.html",
                dados=json.dumps(users_json),
                titulo="Lista de Usuários",
            )

        return redirect("/login")

    @bp.route("/update-user/<id>", methods=["POST", "GET"])
    def update_user(id):
        if session:
            try:
                if request.method == "GET":
                    statementUser = select(Users).where(Users.id == id)
                    usuario: Users = Database().get_one(statementUser)
                    return render_template(
                        "update_users.html", titulo="Editar Usuário", users=usuario
                    )

                statementUser = select(Users).where(Users.id == id)
                usuario: Users = Database().get_one(statementUser)
                data = request.form
                if data:
                    if data["gender"] == "male":
                        usuario.gender = GenderEnum.MALE
                    else:
                        usuario.gender = GenderEnum.FEMALE
                    if data.get("active"):
                        usuario.active = True
                    else:
                        usuario.active = False
                    usuario.fullName = data["fullName"]
                    usuario.password = hash_password(data["password"])
                    usuario.document = data["document"]
                    usuario.userGroupId = data["userGroupId"]
                    Database().save(usuario)

                    return redirect("/list-users")

            except Exception as e:
                print(f"ERRO NO EXCEPTION {e}")
                return abort(400)

        return make_response("Accesso denied", 401)

    @staticmethod
    def check_user_exist(user: str):
        statement_user = select(Users).where(Users.user == user)
        usuario: Users = Database().get_one(statement_user)

        try:
            if usuario is None:
                return False

            return True
        except:
            return abort(400)

    @staticmethod
    @bp.route("/create-admin-user", methods=["POST"])
    def create_admin_user():
        password = hash_password("senhapadrao@123")
        user = UsuarioCtrl.check_user_exist("admin@admin.com")
        if user is False:
            usuario = Users(
                user="admin@admin.com",
                password=password,
                fullName="User Admin",
                document="12345679821",
                gender=GenderEnum.MALE,
            )
            Database().save(usuario)
            return make_response("Sucesso", 200)

    @bp.route("/delete-user/<id>")
    def delete_user(id):
        if session:
            try:
                statement_user = select(Users).where(Users.id == id)
                user: Users = Database().get_one(statement_user)
                print("Checking user")
                if user:
                    Database().delete(user)
                    print(f"User deleted: {user}")
                    return redirect("/list-users")

            except Exception as e:
                return make_response(f"Exception deleted user: {e}", 400)

        return make_response("Access denied", 401)
