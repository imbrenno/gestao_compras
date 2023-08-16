import json
from main.database.models.users.user_groups_models import UserGroups
from main.database.models.database import Database, select
from flask import (
    jsonify,
    Blueprint,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
)


bp = Blueprint(
    "userGroups",
    __name__,
    template_folder="templates",
)


class UserGroupsCtrl:
    @bp.route("/list-groups")
    def get_all_groups():
        if session:
            statement = select(UserGroups)
            groups = Database().get_all(statement)
            groups_json = []
            for group in groups:
                groups_json.append(
                    {
                        "id": group.id,
                        "groupName": group.groupName,
                        "active": group.active,
                    }
                )

            return render_template(
                "list_groups.html",
                groups=json.dumps(groups_json),
                titulo="Grupos de Usuários",
            )
        return redirect("/login")

    @bp.route("/create-group", methods=["POST"])
    def create_group():
        if session:
            try:
                data = request.form
                if data:
                    group = UserGroups(
                        groupName=data["groupName"],
                    )
                    Database().save(group)
                    return redirect("/list-groups")
                return make_response("Bad Rquest", 400)

            except Exception as e:
                print(f"Exception: {e}")
                return make_response("Internal Server Error", 500)
        return redirect("/login")
