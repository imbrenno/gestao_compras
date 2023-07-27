from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.customers_model import Customers
from main.utils.enums.users import GenderEnum

bp = Blueprint(
    "customers",
    __name__,
    template_folder="templates",
)


class CustomerCtrl:

    @bp.route('/list_customers')
    def customers_all():
        if session:
            statement_customers = select(Customers)
            customers = Database().get_all(statement_customers)
            return render_template('customers.html', customers=customers, titulo='Lista de Clientes')

    @bp.route('/create_customers', methods=['GET', 'POST'])
    def create_user():
        if session:
            if request.method == 'GET':
                return render_template('create_customer.html', titulo='Novo Cliente')

            try:
                data = request.form
                print(f'printou data: {data}')

                if data:
                    customer = Customers(
                        companyName=data["companyName"],
                        tradingName=data["tradingName"],
                        vat=data["vat"],
                        representative=data["representative"],
                        contact=data["contact"],
                        address=data["address"],
                        walletManagerId=data["walletManagerId"]

                    )
                    Database().save(customer)
                    return redirect('/list_customers')

                else:
                    return make_response(jsonify({"menssage": "Cliente ja existe"}), 409)
            except Exception as e:
                print(e)
                return make_response('Bad Request', 400)
