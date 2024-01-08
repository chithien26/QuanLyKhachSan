from flask_admin import Admin, AdminIndexView
from app import db, app
from app.models import Phong, KhachHang, NhanVien, TaiKhoan, DonDatPhong, ChiTietDonDatPhong, PhieuThuePhong, HoaDon
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class BaseView(ModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    # can_export = True
    # column_searchable_list = ['name', 'mota']


admin = Admin(app=app, name='QUẢN LÝ KHÁCH SẠN', template_mode='bootstrap4')
admin.add_view(BaseView(Phong, db.session, name='Phòng'))
admin.add_view(BaseView(KhachHang, db.session, name='Khách hàng'))
admin.add_view(BaseView(NhanVien, db.session, name='Nhân viên'))
admin.add_view(BaseView(TaiKhoan, db.session, name='Tài khoản'))
admin.add_view(BaseView(DonDatPhong, db.session, name='Đơn đặt phòng'))
admin.add_view(BaseView(ChiTietDonDatPhong, db.session, name='Chi tiết đơn đặt phòng'))
admin.add_view(BaseView(PhieuThuePhong, db.session, name='Phiếu thuê phòng'))
admin.add_view(BaseView(HoaDon, db.session, name='Hóa đơn'))
