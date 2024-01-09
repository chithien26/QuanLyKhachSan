import hashlib
from flask_login import current_user
from app import db
from app.models import Phong, LoaiPhong, TaiKhoan as TK, DonDatPhong, ChiTietDonDatPhong


def get_phong():

    phong = Phong.query.join(LoaiPhong, Phong.MaLoaiPhong == LoaiPhong.MaLoaiPhong).add_columns(LoaiPhong.DonGia,
                                                                                               LoaiPhong.TenLoaiPhong,
                                                                                               LoaiPhong.Image).all()
    for p in phong:
        phong = [p for p in phong if p.TenPhong]
    return phong

def get_user_by_id(user_id):
    return TK.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TK.query.filter(TK.Username.__eq__(username.strip()),
                             TK.Password.__eq__(password)).first()



def add_user(tenTK, username, password, email, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    tk = TK(TenTK=tenTK, Username=username, Password=password, Email=email, Phone=phone)

    # if avatar:
    #     res = cloudinary.uploader.upload(avatar)
    #     print(res)
    #     u.avatar = res['secure_url']

    db.session.add(tk)
    db.session.commit()

def get_taikhoan():
    return TK.query.all()
# def get_phong_by_id(id):
#     return Phong.query.get(id)
def get_loaiphong():
    return LoaiPhong.query.all()



