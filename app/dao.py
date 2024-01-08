from app.models import Phong, LoaiPhong
from app import app, db
import hashlib
from flask_login import current_user
from sqlalchemy import func
import cloudinary.uploader


def load_room():
    products = Phong.query

    # if kw:
    #     products = products.filter(Product.name.contains(kw))
    #
    # if cate_id:
    #     products = products.filter(Product.category_id.__eq__(cate_id))
    #
    # if page:
    #     page = int(page)
    #     page_size = app.config['PAGE_SIZE']
    #     start = (page - 1)*page_size
    #
    #     return products.slice(start, start + page_size)

    return products.all()

def get_phong():
    return Phong.query.join(LoaiPhong, Phong.MaLoaiPhong == LoaiPhong.MaLoaiPhong).add_columns(LoaiPhong.DonGia, LoaiPhong.TenLoaiPhong, LoaiPhong.Image ).all()

