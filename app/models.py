from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime
import hashlib
import json
from flask_login import UserMixin
from sqlalchemy import MetaData


class LoaiTaiKhoan(enum.Enum):
    ADMIN = 1
    NHANVIEN = 2
    KHACHHANG = 3

class LoaiKhachHang(enum.Enum):
    TRONGNUOC = 1
    NUOCNGOAI = 2

class ChucVu(db.Model):
    __tablename__ = 'chucVu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    nhanVien = relationship("NhanVien", backref='chucVu', lazy=True)

    def __str__(self):
        return self.name
class NhanVien(db.Model):
    __tablename__ = "nhanVien"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoNV = Column(String(10), nullable=False)
    tenNV = Column(String(30), nullable=False)
    phone = Column(String(20), nullable=False)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(String(10), nullable=True)
    ngayVaoLam = Column(DateTime, default=datetime.now())
    chucVu = Column(Integer, ForeignKey(ChucVu.id), nullable=False)

    def __str__(self):
        return f"{self.hoNV} {self.tenNV}"


class KhachHang(db.Model):
    __tablename__ = "khachHang"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=True)
    CMND = Column(String(20), nullable=True)
    diaChi = Column(String(50), nullable=True)
    quocTich = Column(String(20), nullable=False)
    loaiKH = Column(Enum(LoaiKhachHang), default=LoaiKhachHang.TRONGNUOC)

    def __str__(self):
        return self.hoTen

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = "taiKhoan"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    donDatPhong = relationship('DonDatPhong', backref='taikhoan', lazy=True)
    binhLuan = relationship('binhLuan', backref='taiKhoan', lazy=True)
    loaiTaiKhoan = Column(Enum(LoaiTaiKhoan), default=LoaiTaiKhoan.KHACHHANG)
    hoaDon = relationship('HoaDon', backref='taiKhoan', lazy=True)
    def __str__(self):
        return self.name

class LoaiPhong(db.Model):
    __tablename__ = "loaiPhong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    donGia = Column(Float, nullable=False)
    image = Column(String(100), nullable=False)

    def __str__(self):
        return self.name
class Phong(db.Model):
    __tablename__ = "phong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), nullable=False, unique=True)
    soKhachToiDa = Column(Integer, nullable=True, default=3)
    moTa = Column(String(100), nullable=True, default='Phòng dành cho 3 khách')
    chiTietDatPhong = relationship('ChiTietDatPhong', backref='phong', lazy=True)
    chiTietPhieuThue = relationship('ChiTietPhieuThue', backref='phong', lazy=True)
    binhLuan = relationship('binhLuan', backref='phong', lazy=True)

    def __str__(self):
        return self.number

class DonDatPhong(db.Model):
    __tablename__ = "donDatPhong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenKH = Column(String(50), nullable=False)
    ngayDatPhong = Column(DateTime, default=datetime.now())
    taiKhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    chiTietDatPhong = relationship('ChiTietDatPhong', backref='donDatPhong', lazy=True)


    def __str__(self):
        return self.tenKH

class ChiTietDatPhong(db.Model):
    __tablename__ = "chiTietDonDatPhong"
    phong_id = Column(Integer, ForeignKey(Phong.id), primary_key=True)
    donDatPhong_id = Column(Integer, ForeignKey(DonDatPhong.id), primary_key=True)
    ngayNhanPhong = Column(DateTime, nullable=False)
    ngayTraPhong = Column(DateTime, nullable=False)


class PhieuThuePhong(db.Model):
    __tablename__ = "phieuThuePhong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayLapPhieu= Column(DateTime, default=datetime.now())
    taiKhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    chiTietPhieuThue = relationship('ChiTietPhieuThue', backref='phieuThuePhong', lazy=True)

class ChiTietPhieuThue(db.Model):
    phong_id = Column(Integer, ForeignKey(Phong.id), primary_key=True)
    phieuThuePhong_id = Column(Integer, ForeignKey(PhieuThuePhong.id), primary_key=True)
    ngayNhanPhong = Column(DateTime, nullable=False)
    ngayTraPhong = Column(DateTime, nullable=False)


ChiTietPhuThu = db.Table('ChiTietPhuThu',
                         Column('hoaDon_id', Integer, ForeignKey('hoaDon.id'), primary_key=True),
                         Column('phuThu_id', Integer, ForeignKey('phuThu.id'), primary_key=True))

class HoaDon(db.Model):
    __tablename__ = "hoaDon"
    id = Column(Integer, primary_key=True, autoincrement=True)
    thanhTien = Column(Float, nullable=False)
    ngayThanhToan = Column(DateTime, default=datetime.now())
    phieuThuePhong = Column(Integer, ForeignKey(PhieuThuePhong.MaPhieuThuePhong), nullable=False)
    daThanhToan = Column(Boolean, default=False)
    taiKhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)

class PhuThu(db.Model):
    __tablename__ = "phuThu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, unique=True)
    heSo = Column(Float, nullable=False)

class BinhLuan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    taiKhoan_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    phong_id = Column(Integer, ForeignKey(Phong.id), nullable=False)
    content = Column(String(100), nullable=False)
    ngayTao = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.TenLoaiPhuThu

def read_json(path):
    with open(path,'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # chucVu = read_json('data/ChucVu.json')
        # for i in chucVu:
        #     a = ChucVu(TenChucVu=i["TenChucVu"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # loaiKhachHang = read_json('data/LoaiKhachHang.json')
        # for i in loaiKhachHang:
        #     a = LoaiKhachHang(TenLoaiKH=i["TenLoaiKH"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # loaiPhong = read_json('data/LoaiPhong.json')
        # for i in loaiPhong:
        #     a = LoaiPhong(TenLoaiPhong=i["TenLoaiPhong"], DonGia=i["DonGia"],Image=i["Image"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # phuThu = read_json('data/PhuThu.json')
        # for i in phuThu:
        #     a = PhuThu(TenLoaiPhuThu=i["TenLoaiPhuThu"], HeSo=i["HeSo"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # khachHang = read_json('data/KhachHang.json')
        # for i in khachHang:
        #     a = KhachHang(HoKH=i["HoKH"], TenKH=i["TenKH"], Phone=i["Phone"],
        #                   CMND=i['CMND'], DiaChi=i['DiaChi'],
        #                   QuocTich=i["QuocTich"],LoaiKH=i["LoaiKH"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # nhanVien = read_json('data/NhanVien.json')
        # for i in nhanVien:
        #     a = NhanVien(HoNV=i["HoNV"], TenNV=i["TenNV"], Phone=i["Phone"],
        #                   NgaySinh=i['NgaySinh'], GioiTinh=i['GioiTinh'],
        #                   NgayVaoLam=i["NgayVaoLam"], ChucVu=i["ChucVu"])
        #     db.session.add(a)
        #     db.session.commit()
        #
        #
        # phong = read_json('data/Phong.json')
        # for i in phong:
        #     a = Phong(TenPhong=i["TenPhong"], SoKhachToiDa=i["SoKhachToiDa"], MoTa=i["MoTa"],MaLoaiPhong=i['MaLoaiPhong'])
        #     db.session.add(a)
        #     db.session.commit()
        #
        # tk = TaiKhoan(TenTK='Admin', Username='admin',
        #               Password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #               Email='admin.@gmail.com', Phone='0987654321', user_role=UserRoleEnum.NHANVIEN)
        # db.session.add(tk)
        # db.session.commit()
