import hashlib
from flask_login import current_user
from app import db, app
from app.models import Phong, LoaiPhong, TaiKhoan as TK, DonDatPhong, ChiTietDonDatPhong, UserRoleEnum, \
    TrangThaiDonDatPhong, HoaDon


def update_phong_as_paid(dondatphong_id):
    # Tìm phòng dựa trên MaPhong trong cơ sở dữ liệu
    don_dat_phong = DonDatPhong.query.get(dondatphong_id)
    if don_dat_phong:
        # Cập nhật trạng thái của các phòng đã đặt trong đơn đặt phòng
        chi_tiet_don_dat = ChiTietDonDatPhong.query.filter_by(MaDonDatPhong=don_dat_phong.MaDonDat).all()
        for chi_tiet in chi_tiet_don_dat:
            phong = Phong.query.get(chi_tiet.MaPhong)
            if phong:
                phong.TrangThai = 'paid'  # Cập nhật trạng thái phòng thành 'paid'
                db.session.commit()

def load_phong(kw=None, from_price=None, to_price=None):
    phong = Phong.query.join(LoaiPhong, Phong.MaLoaiPhong == LoaiPhong.MaLoaiPhong).add_columns(
        Phong.MaPhong, LoaiPhong.DonGia, LoaiPhong.TenLoaiPhong, LoaiPhong.Image
    ).all()

    if kw:
        phong = [p for p in phong if kw.lower() in p.TenLoaiPhong.lower()]

    if from_price:
        phong = [p for p in phong if p.DonGia >= float(from_price)]

    if to_price:
        phong = [p for p in phong if p.DonGia <= float(to_price)]

    return phong

def thong_ke_luot_su_dung_phong_theo_thang(thang):
    return db.session.query(LoaiPhong.TenLoaiPhong, db.func.count(DonDatPhong.MaLoaiPhong)).join(DonDatPhong, LoaiPhong.MaLoaiPhong == DonDatPhong.MaLoaiPhong).filter(db.extract('month', DonDatPhong.NgayDatPhong) == thang).group_by(LoaiPhong.TenLoaiPhong).all()

def add_hoa_don(don_dat_phong_id, thanh_tien):
    don_dat_phong = DonDatPhong.query.get(don_dat_phong_id)
    if don_dat_phong:
        hoa_don = HoaDon(DonDatPhong=don_dat_phong.MaDonDatPhong, ThanhTien = thanh_tien)
        db.session.add(hoa_don)
        db.session.commit()
def load_loai_phong(kw=None, from_price=None, to_price=None):
    loai_phong = LoaiPhong.query
    if kw:
        loai_phong = [p for p in loai_phong if kw.lower() in p.TenLoaiPhong.lower()]

    if from_price:
        loai_phong = [p for p in loai_phong if p.DonGia >= float(from_price)]

    if to_price:
        loai_phong = [p for p in loai_phong if p.DonGia <= float(to_price)]
    return loai_phong

def get_room_by_id(ma_loai_phong):
    return LoaiPhong.query.get(ma_loai_phong)  # Trả về một dòng duy  # Đảm bảo trả về một đối tượng phòng hợp lệ



def get_user_by_id(user_id):
    return TK.query.get(user_id)

def get_order_list(ten=None, sdt=None):
    list_order =  DonDatPhong.query.join(LoaiPhong, LoaiPhong.MaLoaiPhong == DonDatPhong.MaLoaiPhong).add_columns(
        DonDatPhong.MaLoaiPhong, LoaiPhong.TenLoaiPhong, DonDatPhong.NgayNhanPhong, DonDatPhong.MaDonDatPhong, DonDatPhong.trang_thai,
        DonDatPhong.NgayTraPhong, DonDatPhong.NgayDatPhong, LoaiPhong.DonGia,
        DonDatPhong.HoTenNguoiDat, DonDatPhong.Phone).all()

    if ten:
        list_order = [o for o in list_order if ten.lower() in o.HoTenNguoiDat.lower()]

    if sdt:
        list_order = [o for o in list_order if sdt == o.Phone]

    return list_order
def get_order_list_by_user(user_id):
    return (DonDatPhong.query.join(LoaiPhong, LoaiPhong.MaLoaiPhong == DonDatPhong.MaLoaiPhong).add_columns(
        DonDatPhong.MaLoaiPhong, LoaiPhong.TenLoaiPhong, DonDatPhong.NgayNhanPhong, DonDatPhong.MaDonDatPhong, DonDatPhong.trang_thai,
        DonDatPhong.NgayTraPhong, DonDatPhong.NgayDatPhong, LoaiPhong.DonGia, DonDatPhong.HoTenNguoiDat,
        DonDatPhong.Phone).filter(DonDatPhong.TaiKhoan==user_id).all())

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TK.query.filter(TK.Username.__eq__(username.strip()),
                             TK.Password.__eq__(password)).first()

def pay_order(ma_don_dat_phong):
    don_dat_phong = DonDatPhong.query.get(ma_don_dat_phong)
    if don_dat_phong:
        don_dat_phong.trang_thai = TrangThaiDonDatPhong.DA_THANH_TOAN
        db.session.commit()
def get_order_by_id(ma_don_dat_phong):
    return (DonDatPhong.query.join(LoaiPhong, LoaiPhong.MaLoaiPhong == DonDatPhong.MaLoaiPhong).add_columns(
        DonDatPhong.MaLoaiPhong, LoaiPhong.TenLoaiPhong, DonDatPhong.NgayNhanPhong, DonDatPhong.MaDonDatPhong, DonDatPhong.trang_thai,
        DonDatPhong.NgayTraPhong, DonDatPhong.NgayDatPhong, LoaiPhong.DonGia, DonDatPhong.HoTenNguoiDat,
        DonDatPhong.Phone).filter(DonDatPhong.MaDonDatPhong == ma_don_dat_phong).first())
def add_user(tenTK, username, password, email, phone, user_role=UserRoleEnum.KHACHHANG):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    tk = TK(TenTK=tenTK, Username=username, Password=password, Email=email, Phone=phone, user_role=user_role)

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

def add_dondatphong(danhSachPhongDat, ngayNhanPhong, ngayTraPhong, hoTenNguoiDat, phone):
    if danhSachPhongDat:
        donDatPhong = DonDatPhong(MaTK=current_user.id)  # Assuming MaTK is the foreign key to user
        db.session.add(donDatPhong)
        db.session.commit()  # Commit here to generate the `donDatPhong.MaDonDat`

        for c in danhSachPhongDat.values():
            chiTiet = ChiTietDonDatPhong(
                MaPhong=c['MaPhong'],
                MaDonDatPhong=donDatPhong.MaDonDat,
                NgayNhanPhong=ngayNhanPhong,
                NgayTraPhong=ngayTraPhong
            )
            db.session.add(chiTiet)

        db.session.commit()


