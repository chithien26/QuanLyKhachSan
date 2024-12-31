from datetime import datetime

from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import dao
from app import login
from app.admin import *
from app.dao import get_room_by_id, update_phong_as_paid
from app.models import LoaiKhachHang



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/room_list')
def room_list():
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    rooms = dao.load_loai_phong(kw=kw, from_price=from_price, to_price=to_price)
    return render_template('room_list.html', room_list=rooms)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route('/payment/<int:ma_don_dat_phong>', methods=['GET'])
def payment(ma_don_dat_phong):
    order = dao.get_order_by_id(ma_don_dat_phong)
    return render_template('payment.html', order=order)

@app.route('/process_payment/<int:ma_don_dat_phong>', methods=['POST'])
def process_payment(ma_don_dat_phong):
    thanh_tien = request.form.get('thanh_tien')
    dao.pay_order(ma_don_dat_phong)
    dao.add_hoa_don(ma_don_dat_phong, thanh_tien)
    return redirect(url_for('payment_success'))

@app.route('/payment_success', methods=['GET'])
def payment_success():
    return render_template('payment_success.html')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')

@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(tenTK=request.form.get('tenTK'), username=request.form.get('username'), password=password, email=request.form.get('email'), phone=request.form.get('phone'), user_role=request.form.get('user_role'))
            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('/register.html', err_msg=err_msg)

@app.route('/danh-sach-phong-dat')
def danhSachPhongDat():
    ten = request.args.get('ten')
    sdt = request.args.get('sdt')
    if(current_user.is_authenticated and current_user.user_role == UserRoleEnum.KHACHHANG):
        danh_sach_phong_dat = dao.get_order_list_by_user(user_id=current_user.MaTK)
    else:
        danh_sach_phong_dat = dao.get_order_list(ten=ten, sdt=sdt)
    return render_template('danh_sach_phong_dat.html', danh_sach_phong_dat=danh_sach_phong_dat)

@app.route('/room-details/<int:ma_loai_phong>')
def room_details(ma_loai_phong):
    room = get_room_by_id(ma_loai_phong)  # Hàm giả định để lấy thông tin phòng
    return render_template('room_details.html', room=room)



@app.route('/dat-phong/<int:ma_loai_phong>', methods=['GET', 'POST'])
def booking(ma_loai_phong):
    if(current_user.is_authenticated == False):
        return redirect('/login')
    else:
        loai_phong = dao.get_room_by_id(ma_loai_phong)
        if request.method == 'POST':
            ma_loai_phong = ma_loai_phong
            ho_ten_nguoi_dat = request.form['ho_ten_nguoi_dat']
            phone = request.form['phone']
            ngay_nhan = datetime.strptime(request.form['ngay_nhan'], '%Y-%m-%d').date()
            print(ngay_nhan)
            ngay_tra = datetime.strptime(request.form['ngay_tra'], '%Y-%m-%d').date()
            print(ngay_tra)
            ma_loai_khach_hang = request.form['ma_loai_khach_hang']
            phone = request.form['phone']

            ngay_dat_phong = datetime.now()


            loai_khach_hang = LoaiKhachHang.query.get(ma_loai_khach_hang)
            if not loai_khach_hang:
                loai_khach_hang = LoaiKhachHang.query.filter_by(TenLoaiKH='Khách vãng lai').first()


            # khach_hang = KhachHang(HoKH=ho_kh, TenKH=ten_kh, Phone=phone, CMND=cmnd, DiaChi=dia_chi, QuocTich=quoc_tich, LoaiKH=loai_khach_hang.MaLoaiKH)
            # db.session.add(khach_hang)
            # db.session.commit()


            don_dat_phong = DonDatPhong(MaLoaiPhong=ma_loai_phong, NgayDatPhong=ngay_dat_phong, TaiKhoan=current_user.MaTK, NgayNhanPhong=ngay_nhan, NgayTraPhong=ngay_tra, HoTenNguoiDat=ho_ten_nguoi_dat, Phone=phone)
            db.session.add(don_dat_phong)
            db.session.commit()

            return redirect(url_for('index'))

    danh_sach_phong = Phong.query.all()
    danh_sach_loai_khach_hang = LoaiKhachHang.query.all()
    return render_template('booking.html', danh_sach_phong=danh_sach_phong, danh_sach_loai_khach_hang=danh_sach_loai_khach_hang, ma_loai_phong=ma_loai_phong, loai_phong=loai_phong)

if __name__ == "__main__":
    app.run(debug=True)
