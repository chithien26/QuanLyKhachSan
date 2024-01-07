from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class ChuVu(db.Model):
    MaChuVu = Column(Integer, primary_key=True, autoincrement=True)
    TenChucVu = Column(String(30), nullable=False)
    NhanVien = relationship('NhanVien', backref='ChucVu', lazy=True)

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
    ChucVu = Column(Integer, ForeignKey(ChuVu.MaChuVu), nullable=False)
    TaiKhoanNV = relationship('TaiKhoanNhanVien', backref='NhanVien', lazy=True)

class TaiKhoanNhanVien(db.Model):
    MaTK = Column(Integer, primary_key=True, autoincrement=True)
    TenTK = Column(String(20), nullable=False)
    Username = Column(String(20), unique=True, nullable=False)
    Password = Column(String(20), nullable=False)
    Email = Column(String(20), unique=True, nullable=False)
    Phone = Column(String(20), nullable=False)
    MaNV = Column(Integer, ForeignKey(NhanVien.MaNV), nullable=False)

class LoaiKhachHang(db.Model):
    MaLoaiKH = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiKH = Column(String(20), nullable=False)
    KhachHang = relationship('KhachHang',backref='LoaiKhachHang', lazy=True)

class KhachHang(db.Model):
    MaKH = Column(Integer, primary_key=True, autoincrement=True)
    HoKH = Column(String(10), nullable=False)
    TenKH = Column(String(30), nullable=False)
    Phone = Column(String(20), nullable=False)
    CMND = Column(String(20), nullable=False)
    DiaChi = Column(String(50), nullable=True)
    QuocTich = Column(String(20), nullable=False)
    MaKH = Column(Integer, ForeignKey(LoaiKhachHang.MaLoaiKH), nullable=False)
    TaiKhoanKH = relationship('TaiKhoanKhachHang', backref='KhachHang', lazy=True)
    PhieuThuePhong = relationship('PhieuThuePhong', backref='KhachHang', lazy=True)

class TaiKhoanKhachHang(db.Model):
    MaTK = Column(Integer, primary_key=True, autoincrement=True)
    TenTK = Column(String(20), nullable=False)
    Username = Column(String(20), unique=True, nullable=False)
    Password = Column(String(20), nullable=False)
    Email = Column(String(20), unique=True, nullable=False)
    Phone = Column(String(20), nullable=False)
    MaKH = Column(Integer, ForeignKey(KhachHang.MaKH), nullable=False)

class LoaiPhong(db.Model):
    MaLoaiPhong = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiPhong = Column(String(20), nullable=False)
    DonGia = Column(Float, nullable=False)
    Phong = relationship('Phong', backref='LoaiPhong', lazy=True)

class Phong(db.Model):
    MaPhong = Column(Integer, primary_key=True, autoincrement=True)
    TenPhong = Column(String(20), nullable=False)
    SoKhachToiDa = Column(Integer, nullable=True, default=3)
    MoTa = Column(String(100), nullable=True, default='Phòng dành cho 3 khách')
    MaLoaiPhong = Column(Integer, ForeignKey(LoaiPhong.MaLoaiPhong), nullable=False)
    DonDatPhong = relationship('DonDatPhong', backref='Phong', lazy=True)
    ChiTietDonDatPhong = relationship('ChiTietDonDatPhong', backref='Phong', lazy=True)

class DonDatPhong(db.Model):
    MaDonDatPhong = Column(Integer, primary_key=True, autoincrement=True)
    MaPhong = Column(Integer, ForeignKey(Phong.MaPhong), nullable=False)
    NgayDatPhong = Column(DateTime, default=datetime.now())
    DaThanhToan = Column(Boolean, default=False)
    ChiTietDonDatPhong = relationship('ChiTietDonDatPhong', backref='DonDatPhong', lazy=True)

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
    HoaDon = relationship('HoaDon', backref='PhieuThuePhong', lazy=True)

class HoaDon(db.Model):
    MaHoaDon = Column(Integer, primary_key=True, autoincrement=True)
    PhuThu = Column(Float, default=0)
    ThanhTien = Column(Float, nullable=False)
    NgayThanhToan = Column(DateTime, default=datetime.now())
    PhieuThuePhong = Column(Integer, ForeignKey(PhieuThuePhong.MaPhieuThuePhong), nullable=False)
    ChiTietPhuThu = relationship('ChiTietPhuThu', backref='HoaDon', lazy=True)
class PhuThu(db.Model):
    MaPhuThu = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiTaiPhuThu = Column(String(30), nullable=False)
    HeSo = Column(Float, nullable=False)
    ChiTietPhuThu = relationship('ChiTietPhuThu', backref='PhuThu', lazy=True)

class ChiTietPhuThu(db.Model):
    HoaDon = Column(Integer, ForeignKey(HoaDon.MaHoaDon), primary_key=True)
    PhuThu = Column(Integer, ForeignKey(PhuThu.MaPhuThu), primary_key=True)
