from main.database.models.database import Database, select
from flask import jsonify, Blueprint, abort, request, make_response, redirect, render_template, session
from main.database.models.users_model import Users
from main.utils.enums.users import GenderEnum

bp = Blueprint(
    "users",
    __name__,
    template_folder="templates",
)


class UsuarioCtrl:

    @staticmethod
    @bp.route('/create_user', methods=['POST', 'GET'])
    def create_user():
        if session:
            if request.method == 'GET':
                return render_template('create_user.html', titulo='Novo Usuário')

            try:
                data = request.form
                print(data)
                user = UsuarioCtrl.check_user_exist(data["user"])
                if user is False:
                    if data:
                        usuario = Users(
                            user=data["user"],
                            password=data["password"],
                            fullName=data["fullName"],
                            document=data["document"],
                            gender=data["gender"]
                        )
                        Database().save(usuario)

                    return redirect('/list_users')

                else:
                    return make_response(jsonify({"menssage": "Usuario ja existe"}), 409)

            except Exception as e:
                print(e)
                return abort(400)

        else:
            return redirect('/login')
        
        
    @bp.route('/list_users')
    def users_all():
        if session:
            statement = select(Users)
            users = Database().get_all(statement)
            return render_template('list_users.html', users=users, titulo='Lista de Usuários')
        else:
            return redirect('/login')
        

    @bp.route('/update_user/<id>', methods=['POST', 'GET'])
    def update_user(id):
        if session:
            try:
                if request.method == 'GET':
                    statement_user = select(Users).where(Users.id == id)
                    print('passou do statement')
                    usuario: Users = Database().get_one(statement_user) 
                    print('passou do usuario')
                    return render_template('update_users.html', titulo='Editar Usuário', users=usuario)

                
                statement_user = select(Users).where(Users.id == id)
                usuario: Users = Database().get_one(statement_user)
                data = request.form
                if data:
                    if data['gender'] == 'male':
                        usuario.gender = GenderEnum.MALE
                    else:
                        usuario.gender = GenderEnum.FEMALE
                    if data.get('active'):
                         usuario.active = True
                    else:
                        usuario.active = False
                    usuario.fullName = data["fullName"]
                    usuario.password = data["password"]
                    usuario.document = data["document"]
                    Database().save(usuario)

                    return redirect('/list_users')

            except Exception as e:
                print(F'ERRO NO EXCEPTION {e}')
                return abort(400)
        
        else:
            return make_response('Acesso negado', 401)
        

    @staticmethod
    def check_user_exist(user: str):

        statement_user = select(Users).where(Users.user == user)
        usuario: Users = Database().get_one(statement_user)

        try:
            if usuario is None:
                return False
            else:
                return True
        except:
            return abort(400)
