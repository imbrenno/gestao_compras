from json import dumps
from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.customers_model import Customers
from main.utils.utils import encode_addrees


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
            return render_template('list_customers.html', customers=customers, titulo='Clientes')
        

    @bp.route('/create_customers', methods=['GET', 'POST'])
    def create_user():
        if session:
            if request.method == 'GET':
                return render_template('create_customer.html', titulo='Cadastrar Novo Cliente')

            try:
                data = request.form
                addrees = data
                if data:
                    customer = Customers(
                        companyName=data["companyName"],
                        tradingName=data["tradingName"],
                        vat=data["vat"],
                        representative=data["representative"],
                        contact=data["contact"],
                        address=encode_addrees(addrees),
                        walletManagerId=data["walletManagerId"]

                    )
                    Database().save(customer)
                    return redirect('/list_customers')

                else:
                    return make_response(jsonify({"menssage": "Cliente ja existe"}), 409)
            except Exception as e:
                print(e)
                return make_response('Bad Request', 400)


    @bp.route('/update_customer/<id>', methods=['POST', 'GET'])
    def update_user(id):
        if session:
            try:
                if request.method == 'GET':
                    statement_customer = select(Customers).where(Customers.id == id)
                    print('passou do statement')
                    customer: Customers = Database().get_one(statement_customer)
                    print('passou do customer')
                    return render_template('update_customers.html', titulo='Editar Cliente', customers=customer)

                
                statement_customer = select(Customers).where(Customers.id == id)
                customer: Customers = Database().get_one(statement_customer)

                data = request.form
                if data:
                    if data.get('active'):
                        customer.active = True
                    else:
                        customer.active = False
                    customer.companyName = data["companyName"]
                    customer.tradingName = data["tradingName"]
                    customer.vat = data["vat"]
                    customer.representative = data["representative"]
                    customer.contact = data["contact"]
                    customer.address = dumps(data["address"])
                    customer.walletManagerId = data["walletManagerId"]


                    Database().save(customer)

                    return redirect('/list_customers')

            except Exception as e:
                print(e)
                return abort(400)
        
        else:
            return make_response('Acesso negado', 401)