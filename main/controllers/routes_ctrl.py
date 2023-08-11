from main.database.models.database import Database, select
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
from main.database.models.users.routes_models import Routes

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
                return make_response('Registered route', 200)
        except Exception as e:
            print(f"Exception: {e}")
            return make_response("Internal Server Error", 500)
        
    @bp.route("/list-routes")
    def list_routes():
        if session:
            statement_routes = select(Routes)
            routes : Routes = Database().get_all(statement_routes)
            return render_template("list_routes.html", titulo="Lista de Rotas", routes=routes)

