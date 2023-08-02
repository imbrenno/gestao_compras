from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.supplier_model import Suppliers
from main.utils.utils import decode_str, encode_addrees, encode_contact


bp = Blueprint(
    "suppiers",
    __name__,
    template_folder="templates",
)


class SuppliersCtrl:

    @bp.route('/list-suppliers')
    def list_suppliers():
        if session:
            return render_template('list_suppliers.html', titulo='Lista de Fornecedores')