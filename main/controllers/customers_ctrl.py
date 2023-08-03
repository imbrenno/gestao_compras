from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.customers_model import Customers
from main.utils.utils import decode_str, encode_addrees, encode_contact


bp = Blueprint(
    "customers",
    __name__,
    template_folder="templates",
)


class CustomerCtrl:

    @bp.route('/list-customers')
    def customers_all():
        if session:
            statement_customers = select(Customers)
            customers = Database().get_all(statement_customers)
            return render_template('list_customers.html', customers=customers, titulo='Clientes')
        

    @bp.route('/create-customers', methods=['GET', 'POST'])
    def create_user():
        if session:
            if request.method == 'GET':
                return render_template('create_customer.html', titulo='Cadastrar Novo Cliente')

            try:
                data = request.form
                addrees = data
                contact = data
                if data:
                    customer = Customers(
                        companyName=data["companyName"],
                        tradingName=data["tradingName"],
                        vat=data["vat"],
                        representative=data["representative"],
                        contact=encode_contact(contact),
                        address=encode_addrees(addrees),
                        walletManagerId=data["walletManagerId"]

                    )
                    Database().save(customer)
                    return redirect('/list-customers')

                else:
                    return make_response(jsonify({"menssage": "Cliente ja existe"}), 409)
            except Exception as e:
                print(e)
                return make_response('Bad Request', 400)


    @bp.route('/update-customer/<id>', methods=['POST', 'GET'])
    def update_user(id):
        if session:
            try:
                if request.method == 'GET':
                    statementCustomer = select(Customers).where(Customers.id == id)
                    customer: Customers = Database().get_one(statementCustomer)
                    customerAddrees = decode_str(customer.address)
                    customerContact = decode_str(customer.contact)
                    print(f'printando rua: {customerAddrees["street"]}')
                    print(f'printando rua: {customerContact["cell"]}')

                    print(f'passou do customer: {customerAddrees}')
                    return render_template('update_customers.html', titulo='Editar Cliente', customers=customer, customersAddrees=customerAddrees, customerContact=customerContact)

                
                statementCustomer = select(Customers).where(Customers.id == id)
                customer: Customers = Database().get_one(statementCustomer)

                data = request.form
                addrees = data
                contact = data
                if data:
                    if data.get('active'):
                        customer.active = True
                    else:
                        customer.active = False
                    customer.companyName = data["companyName"]
                    customer.tradingName = data["tradingName"]
                    customer.vat = data["vat"]
                    customer.representative = data["representative"]
                    customer.contact = encode_contact(contact)
                    customer.address = encode_addrees(addrees)
                    customer.walletManagerId = data["walletManagerId"]


                    Database().save(customer)

                    return redirect('/list-customers')

            except Exception as e:
                print(e)
                return abort(400)
        
        else:
            return make_response('Acesso negado', 401)