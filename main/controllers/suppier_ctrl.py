from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.supplier_model import Suppliers
from main.utils.utils import decode_str, encode_addrees, encode_contact
from main.utils.enums.supplier import SuplierPaymentTypesEnum


bp = Blueprint(
    "suppiers",
    __name__,
    template_folder="templates",
)


class SuppliersCtrl:

    @bp.route('/list-suppliers')
    def list_suppliers():
        if session:
            statement_supplier = select(Suppliers)
            suppliers = Database().get_all(statement_supplier)
            return render_template('list_suppliers.html', titulo='Lista de Fornecedores', suppliers=suppliers)

        return make_response('Access Denied', 401)
    
    @bp.route('/create-supplier', methods=['POST', 'GET'])
    def create_supplier():
        if session:
            try:
                
                if request.method == 'GET':
                    return render_template('create_supplier.html', titulo='Cadastrar Fornecedor')
                
                data = request.form
                print(f'printando: {data}')
                if data:
                    supplier = Suppliers(
                        companyName=data['companyName'],
                        tradingName=data['tradingName'],
                        vat=data['vat'],
                        representative=data['representative'],
                        contact=encode_contact(data),
                        address=encode_addrees(data),
                        category=data['category'],
                        paymentTypes=data['paymentTypes'],            
                        walletManagerId=int(data['walletManagerId'])

                    )
                    print(f'supplier: {supplier}')
                    Database().save(supplier)
                    return redirect('/list-suppliers')
                    
            except Exception as e:
                print(f'Erro ao criar supplier {e}')
                return abort(400)
        else:
            return make_response('Access Denied', 401)



    @bp.route('/update-supplier/<id>', methods=['POST', 'GET'])
    def update_user(id):
        if session:
            try:
                if request.method == 'GET':
                    statement_supplier = select(Suppliers).where(Suppliers.id == id)
                    supplier: Suppliers = Database().get_one(statement_supplier)
                    supplier_addrees = decode_str(supplier.address)
                    supplier_contact = decode_str(supplier.contact)
                    return render_template('update_supplier.html', titulo='Editar Forncedor', suppliers=supplier, suppliersAddrees=supplier_addrees, supplierContact=supplier_contact)

                
                statement_supplier = select(Suppliers).where(Suppliers.id == id)
                supplier: Suppliers = Database().get_one(statement_supplier)

                data = request.form
                if data:
                    if data.get('active'):
                        supplier.active = True
                    else:
                        supplier.active = False
                    supplier.companyName = data["companyName"]
                    supplier.tradingName = data["tradingName"]
                    supplier.vat = data["vat"]
                    supplier.representative = data["representative"]
                    supplier.contact = encode_contact(data)
                    supplier.address = encode_addrees(data)
                    supplier.category = data["category"]
                    supplier.paymentTypes = data["paymentTypes"]
                    supplier.walletManagerId = data["walletManagerId"]


                    Database().save(supplier)
                    return redirect('/list-suppliers')
                
                return abort(400)
            except Exception as e:
                print(e)
                return abort(400)
        
        return make_response('Access Denied', 401)
        

    @bp.route('/delete-supplier/<id>', methods=['POST'])
    def delete_supplier(id):
        if session:
            try:    
                statement_supplier = select(Suppliers).where(Suppliers.id == id)
                supplier : Suppliers = Database().get_one(statement_supplier)
                print(f'Supplier para deletar: {supplier}')
                if supplier:
                    Database().delete(supplier)
                    return redirect('/list-suppliers')
                
                return make_response('Supplier not found', 404)
            
            except Exception as e:
                print(f'Exception delet supplier: {e}')
                return abort(400)
            
        return make_response('Access Denied', 401)