from app import admin, db
from app.models import Phong, LoaiPhong, KhachHang, NhanVien, TaiKhoanKhachHang, TaiKhoanNhanVien, DonDatPhong, PhieuThuePhong, ChiTietDonDatPhong, HoaDon
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(LoaiPhong, db.session))

admin.add_view(ModelView(Phong, db.session))
admin.add_view(ModelView(KhachHang, db.session))
admin.add_view(ModelView(NhanVien, db.session))
