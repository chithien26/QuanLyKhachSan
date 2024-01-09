function addToCart(MaPhong, TenPhong, DonGia) {
    fetch('/api/danhSachPhongDat', {
        method: 'post',
        body: JSON.stringify({
            "MaPhong": MaPhong,
            "TenPhong": TenPhong,
            "DonGia": DonGia
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity
    });
}
