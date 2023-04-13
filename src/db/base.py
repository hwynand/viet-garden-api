# Import all the models, so that Alembic can read from memory
# and auto generate migration
# https://stackoverflow.com/questions/15660676/alembic-autogenerate-producing-empty-migration
from db.base_model import Base
from models.cart import CartProduct
from models.category import Category, CategoryGroup
from models.product import Product, ProductImage
from models.user import User
