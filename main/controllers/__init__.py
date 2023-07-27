from .index_ctrl import bp as index_bp
from .users_ctrl import bp as users_bp
from .login_ctrl import bp as login_bp
from .customers_ctrl import bp as customers_bp

blueprints_ctrl = [
    index_bp,
    users_bp,
    login_bp,
    customers_bp
]
