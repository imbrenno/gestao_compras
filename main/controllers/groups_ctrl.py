import json
from typing import List

from main.database.models.users.user_groups_model import UserGroups
from main.database.models.database import Database, select
from main.database.models.users.group_permissions_model import GroupPermissions
from main.database.models.users.routes_model import Routes
from flask import (
    abort,
    Blueprint,
    jsonify,
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
    
    @bp.route("/list-routes-group/<id>")
    def get_all_routes_group(id):
        if session:
            statement = select(GroupPermissions).where(GroupPermissions.userGroupsId == id)
            user_group = Database().get_all(statement)
            print(f"USER_GROUP: {user_group}", type(user_group))
            routes_group_json = []
            for u in user_group:
                statement_route = select(Routes).where(Routes.id == u.routeId)
                route = Database().get_one(statement_route)
                routes_group_json.append(
                    {
                        "routeId": route.id,
                        "routeName": route.routeName
                    }
                )
            print(f"ROUTES_GROUP: {routes_group_json}", type(routes_group_json))
            return render_template(
                "list_groups.html",
                routesGroups=json.dumps(routes_group_json),
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

    @staticmethod
    @bp.route("/register-routes-group", methods=["POST"])
    def register_routes_in_group():
        if session:
            try:
                data = request.json
                print(f"DATA: {data}", type(data))

                if data:
                    for d in data:
                        check_group_permission = UserGroupsCtrl.check_permission_group(
                            d["userGroupsId"], d["id"]
                        )
                        if check_group_permission:
                            group_permissions = GroupPermissions(
                                userGroupsId=d["userGroupsId"], routeId=d["id"]
                            )
                            print(
                                f"SAVE_GROUP_PERMISSION: {group_permissions}",
                                type(group_permissions),
                            )
                            Database().save(group_permissions)
                            print("200")

                    return make_response("SUCCESS", 200)
                return make_response("BAD REQUEST", 400)

            except Exception as e:
                print(f"Exception: {e}")
                return make_response("INTERNAL_SERVER_ERROR", 500)
        return redirect("/login")

    @bp.route("/delete-route-group/<id>")
    def delete_route_group(id):
        if session:
            statement = select(GroupPermissions).where(GroupPermissions.id == id)
            group_permission: GroupPermissions = Database().get_one(statement)
            print(f"group_permission: {group_permission}")
            if group_permission:
                Database().delete(group_permission)
                return make_response("SUCCESS", 200)
            print(f"THERE_IS_NO_PERMISSION_FOR_GROUP")
            return make_response("NOT FOUND", 404)

    @staticmethod
    def check_permission_group(userGroupsId, routeId):
        statement = select(GroupPermissions).where(
            GroupPermissions.userGroupsId == userGroupsId,
            GroupPermissions.routeId == routeId,
        )
        group_permission: List[GroupPermissions] = Database().get_all(statement)
        print(f"group_permission: {group_permission}")
        if not group_permission:
            print(f"THERE_IS_NO_PERMISSION_FOR_GROUP")
            return True
        print(f"PERMISSION_ALREADY_EXISTS_FOR_GROUP")
        return False
