from main.database.models.database import Database, select
from flask import (
    Blueprint,
    request,
    make_response,
    redirect,
    render_template,
    session,
)
from main.database.models.users.routes_model import Routes
import json

bp = Blueprint("routes", __name__, template_folder="templates")


class RoutesCtrl:
    @bp.route("/create-route", methods=["POST"])
    def create_route():
        try:
            data = request.json
            if data:
                route = Routes(
                    routeName=data["routeName"],
                    route=data["route"],
                )
                Database().save(route)
                return make_response("Registered route", 200)
        except Exception as e:
            print(f"Exception: {e}")
            return make_response("Internal Server Error", 500)

    @bp.route("/list-routes")
    def list_all_routes():
        if session:
            statement_routes = select(Routes)
            routes = Database().get_all(statement_routes)
            routes_json = []
            for route in routes:
                routes_json.append(
                    {
                        "id": route.id,
                        "routeName": route.routeName,
                        "route": route.route,
                    }
                )
            return json.dumps(routes_json), 200
        
        return redirect("/login")

