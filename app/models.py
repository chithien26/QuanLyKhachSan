from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime
import hashlib
import json



class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class ChucVu(db.Model):
    MaChucVu = Column(Integer, primary_key=True, autoincrement=True)
    TenChucVu = Column(String(30), nullable=False, unique=True)
    NhanVien = relationship('NhanVien', backref='chucVu', lazy=True)

    def __str__(self):
        return self.TenChucVu

class NhanVien(db.Model):
    MaNV = Column(Integer, primary_key=True, autoincrement=True)
    HoNV = Column(String(10), nullable=False)
    TenNV = Column(String(30), nullable=False)
    Phone = Column(String(20), nullable=False)
    NgaySinh = Column(DateTime, nullable=False)
    GioiTinh = Column(String(10), nullable=False)
    NgayVaoLam = Column(DateTime, default=datetime.now())
    ChucVu = Column(Integer, ForeignKey(ChucVu.MaChucVu), nullable=False)
    TaiKhoanNV = relationship('TaiKhoanNhanVien', backref='nhanVien', lazy=True)

    def __str__(self):
        return self.TenNV

class TaiKhoanNhanVien(db.Model):
    MaTK = Column(Integer, primary_key=True, autoincrement=True)
    TenTK = Column(String(20), nullable=False)
    Username = Column(String(20), unique=True, nullable=False)
    Password = Column(String(20), nullable=False)
    Email = Column(String(50), unique=True, nullable=False)
    Phone = Column(String(20), nullable=False)
    MaNV = Column(Integer, ForeignKey(NhanVien.MaNV), nullable=False)

    def __str__(self):
        return self.TenTK

class LoaiKhachHang(db.Model):
    MaLoaiKH = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiKH = Column(String(20), nullable=False)
    KhachHang = relationship('KhachHang',backref='loaiKhachHang', lazy=True)

    def __str__(self):
        return self.TenLoaiKH

class KhachHang(db.Model):
    MaKH = Column(Integer, primary_key=True, autoincrement=True)
    HoKH = Column(String(10), nullable=False)
    TenKH = Column(String(30), nullable=False)
    Phone = Column(String(20), nullable=False)
    CMND = Column(String(20), nullable=False)
    DiaChi = Column(String(50), nullable=True)
    QuocTich = Column(String(20), nullable=False)
    LoaiKH = Column(Integer, ForeignKey(LoaiKhachHang.MaLoaiKH), nullable=False)
    TaiKhoanKH = relationship('TaiKhoanKhachHang', backref='khachHang', lazy=True)
    PhieuThuePhong = relationship('PhieuThuePhong', backref='khachHang', lazy=True)

    def __str__(self):
        return self.TenKH

class TaiKhoanKhachHang(db.Model):
    MaTK = Column(Integer, primary_key=True, autoincrement=True)
    TenTK = Column(String(20), nullable=False)
    Username = Column(String(20), unique=True, nullable=False)
    Password = Column(String(20), nullable=False)
    Email = Column(String(50), unique=True, nullable=False)
    Phone = Column(String(20), nullable=False)
    MaKH = Column(Integer, ForeignKey(KhachHang.MaKH), nullable=False)

    def __str__(self):
        return self.TenTK

class LoaiPhong(db.Model):
    MaLoaiPhong = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiPhong = Column(String(20), nullable=False, unique=True)
    DonGia = Column(Float, nullable=False)
    Image = Column(String(100), nullable=False)
    Phong = relationship('Phong', backref='loaiPhong', lazy=True)

    def __str__(self):
        return self.TenLoaiPhong
class Phong(db.Model):
    MaPhong = Column(Integer, primary_key=True, autoincrement=True)
    TenPhong = Column(String(20), nullable=False, unique=True)
    SoKhachToiDa = Column(Integer, nullable=True, default=3)
    MoTa = Column(String(100), nullable=True, default='Phòng dành cho 3 khách')
    MaLoaiPhong = Column(Integer, ForeignKey(LoaiPhong.MaLoaiPhong), nullable=False)
    DonDatPhong = relationship('DonDatPhong', backref='phong', lazy=True)
    ChiTietDonDatPhong = relationship('ChiTietDonDatPhong', backref='phong', lazy=True)

    def __str__(self):
        return self.TenPhong

class DonDatPhong(db.Model):
    MaDonDatPhong = Column(Integer, primary_key=True, autoincrement=True)
    MaPhong = Column(Integer, ForeignKey(Phong.MaPhong), nullable=False)
    NgayDatPhong = Column(DateTime, default=datetime.now())
    ChiTietDonDatPhong = relationship('ChiTietDonDatPhong', backref='donDatPhong', lazy=True)

    def __str__(self):
        return self.MaDonDatPhong

class ChiTietDonDatPhong(db.Model):
    MaPhong = Column(Integer, ForeignKey(Phong.MaPhong), primary_key=True)
    MaDonDatPhong = Column(Integer, ForeignKey(DonDatPhong.MaDonDatPhong), primary_key=True)
    NgayNhanPhong = Column(DateTime, nullable=False)
    NgayTraPhong = Column(DateTime, nullable=False)

class PhieuThuePhong(db.Model):
    MaPhieuThuePhong = Column(Integer, primary_key=True, autoincrement=True)
    NgayNhanPhong = Column(DateTime, nullable=False)
    NgayTraPhong = Column(DateTime, nullable=False)
    SoLuongKhach = Column(Integer, nullable=False)
    KhachHang = Column(Integer, ForeignKey(KhachHang.MaKH), nullable=False)
    HoaDon = relationship('HoaDon', backref='phieuThuePhong', lazy=True)



ChiTietPhuThu = db.Table('ChiTietPhuThu',
                         Column('MaHoaDon', Integer, ForeignKey('hoaDon.MaHoaDon'), primary_key=True),
                         Column('MaPhuThu', Integer, ForeignKey('phuThu.MaPhuThu'), primary_key=True))

class HoaDon(db.Model):
    __tablename__ = "hoaDon"
    MaHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    ThanhTien = Column(Float, nullable=False)
    NgayThanhToan = Column(DateTime, default=datetime.now())
    PhieuThuePhong = Column(Integer, ForeignKey(PhieuThuePhong.MaPhieuThuePhong), nullable=False)
    DaThanhToan = Column(Boolean, default=False)
    CacPhuThu = relationship('PhuThu', secondary='ChiTietPhuThu', lazy='subquery', backref=backref('hoaDon',lazy=True))


class PhuThu(db.Model):
    __tablename__ = "phuThu"
    MaPhuThu = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiPhuThu = Column(String(30), nullable=False, unique=True)
    HeSo = Column(Float, nullable=False)

    def __str__(self):
        return self.TenLoaiPhuThu

def read_json(path):
    with open(path,'r') as f:
        return json.load(f)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        chucVu = read_json('data/ChucVu.json')
        for i in chucVu:
            a = ChucVu(TenChucVu=i["TenChucVu"])
            db.session.add(a)
            db.session.commit()

        loaiKhachHang = read_json('data/LoaiKhachHang.json')
        for i in loaiKhachHang:
            a = LoaiKhachHang(TenLoaiKH=i["TenLoaiKH"])
            db.session.add(a)
            db.session.commit()

        loaiPhong = read_json('data/LoaiPhong.json')
        for i in loaiPhong:
            a = LoaiPhong(TenLoaiPhong=i["TenLoaiPhong"], DonGia=i["DonGia"],Image=i["Image"])
            db.session.add(a)
            db.session.commit()

        phuThu = read_json('data/PhuThu.json')
        for i in phuThu:
            a = PhuThu(TenLoaiPhuThu=i["TenLoaiPhuThu"], HeSo=i["HeSo"])
            db.session.add(a)
            db.session.commit()

        khachHang = read_json('data/KhachHang.json')
        for i in khachHang:
            a = KhachHang(HoKH=i["HoKH"], TenKH=i["TenKH"], Phone=i["Phone"],
                          CMND=i['CMND'], DiaChi=i['DiaChi'],
                          QuocTich=i["QuocTich"],LoaiKH=i["LoaiKH"])
            db.session.add(a)
            db.session.commit()

        nhanVien = read_json('data/NhanVien.json')
        for i in nhanVien:
            a = NhanVien(HoNV=i["HoNV"], TenNV=i["TenNV"], Phone=i["Phone"],
                          NgaySinh=i['NgaySinh'], GioiTinh=i['GioiTinh'],
                          NgayVaoLam=i["NgayVaoLam"], ChucVu=i["ChucVu"])
            db.session.add(a)
            db.session.commit()


        phong = read_json('data/Phong.json')
        for i in phong:
            a = Phong(TenPhong=i["TenPhong"], SoKhachToiDa=i["SoKhachToiDa"], MoTa=i["MoTa"],MaLoaiPhong=i['MaLoaiPhong'])
            db.session.add(a)
            db.session.commit()

        taiKhoanKhachHang = read_json('data/TaiKhoanKhachHang.json')
        for i in taiKhoanKhachHang:
            a = TaiKhoanKhachHang(TenTK=i["TenTK"], Username=i["Username"], Password=i["Password"],
                                  Email=i['Email'], Phone=i['Phone'],MaKH=i["MaKH"])
            db.session.add(a)
            db.session.commit()

        taiKhoanNhanVien = read_json('data/TaiKhoanNhanVien.json')
        for i in taiKhoanNhanVien:
            a = TaiKhoanNhanVien(TenTK=i["TenTK"], Username=i["Username"], Password=i["Password"],
                                  Email=i['Email'], Phone=i['Phone'], MaNV=i["MaNV"])
            db.session.add(a)
            db.session.commit()