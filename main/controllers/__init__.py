from .index_ctrl import bp as index_bp
from .users_ctrl import bp as users_bp
from .login_ctrl import bp as login_bp
from .customers_ctrl import bp as customers_bp
from .suppliers_ctrl import bp as suppliers_bp
from .routes_ctrl import bp as routes_bp
from .groups_ctrl import bp as groups_bp

blueprints_ctrl = [
    index_bp,
    users_bp,
    login_bp,
    customers_bp,
    suppliers_bp,
    routes_bp,
    groups_bp,

]
