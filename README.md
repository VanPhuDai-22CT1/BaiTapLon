# Hệ thống Tự động Tra cứu Phương tiện Vi phạm Giao thông

Một công cụ tự động tra cứu phương tiện vi phạm từ website Cục Cảnh sát Giao thông Việt Nam bằng Python.

##  Tính năng
- Tự động mở trình duyệt và truy cập trang tra cứu.
- Nhập biển số và loại phương tiện.
- Tự động nhận diện mã CAPTCHA bằng OCR.
- In kết quả vi phạm (nếu có) ra màn hình.
- Lên lịch chạy tự động mỗi ngày lúc 06:00 và 12:00.

---

##  Yêu cầu hệ thống
- Python 3.8+
- Google Chrome đã cài đặt sẵn
- Tesseract OCR

---

##  Cài đặt

### 1. Clone project
```bash
git clone https://github.com/VanPhuDai-22CT1/BaiTapLon.git
cd 'c:\BaiTapLon_TuDongHoaQuyTrinh
```
---

### 2. Cài đặt Tesseract OCR
 Windows:
Tải và cài đặt tại: https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0
Khi Tải về Song Chúng Ta Sẽ Được 1 thư mục ở dạng .zip:
![image](https://github.com/user-attachments/assets/6023de7c-0bc7-49b7-8cd2-b71d3ca6f6ee)


![](./Hinhanh/01.jpg)

Chúng ta thực hiện quy trình giải nén và cài vào dự án của mình:
+ Như ở dự án của mình thì cài đặt nào và đặt tên thư mục là (New folder)
+ và có Đường dẫn:
```bash
 C:\BaiTapLon_TuDongHoaQuyTrinh\New folder\tesseract.exe
```
---

### 3. Cài đặt thư viện Python
 Mở Terminal trong VSCode:
 + thực hiện nhấn tổ hợp phím:(Ctrl+Shift+`).
 + Terminal sex mở cái thư mục của dự án mình lên.
 + Sẽ chạy lệnh ở bên dưới và hệ thống sẽ thực hiện tuyến trình cài đặt.
```bash
pip install -r requirements.txt
```
---
# Cách Sử Dụng 
### 1.Chọn biển số để tra:
Trong file phatnguoi.py, có thể chỉnh sửa biển số theo bạn mong muốn:
```bash
VEHICLES = [
    ("47F00171", "Ô tô"),
    ("98D1-60554", "Xe máy")
]
```
---
### 2.thự hiện quy trình chạy trong TERMINAL:
+ thực hiện chạy chương trình.
```bash
python phatnguoi.py
```
+ khi thực hiện quy trình chạy thì sẽ hiện ra một thông báo:
--> Hệ thống sẽ tra cứu tự động lúc 6h và 12h mỗi ngày cho ô tô và xe máy.
+ Khi Không tìm thấy được mã captcha thì sẽ hiện thông báo:
```bash
Thử lần 2 cho Xe máy 98D1-60554
[OK] Nhận diện captcha thành công: 6vg82m
Không có dữ liệu hoặc sai captcha.
```
+ Khi Tìm xa được xe vi phạm thì sẽ hiện ra thông báo:
+ Gồm có: thông tin vi phạm , thời gian , địa điểm , tổ công tác thực , thông tổ cồng tác,... 
```bash
Thử lần 3 cho Ô tô 47F00171
[OK] Nhận diện captcha thành công: pwd39q
[KẾT QUẢ] Đã tìm thấy vi phạm cho Ô tô 47F00171
Biển kiểm soát:47F-001.71
Màu biển:Nền màu vàng, chữ và số màu đen
Loại phương tiện:Ô tô
Thời gian vi phạm:04:59, 22/01/2024
Địa điểm vi phạm:
Đường Lê Duẩn hướng Cầu Trắng về thành phố, Phường Ea Tam, Thành phố Buôn Ma Thuột, Tỉnh Đắk Lắk
Hành vi vi phạm:
12321.5.6.a.01.Điều khiển xe chạy quá tốc độ quy định trên 20 km/h đến 35 km/h
Trạng thái:
ĐÃ XỬ PHẠT
Đơn vị phát hiện vi phạm: ĐỘI TT, ĐTGQTNGT VÀ XLVP - PHÒNG CSGT ĐẮK LẮK
Nơi giải quyết vụ việc: 1. ĐỘI TT, ĐTGQTNGT VÀ XLVP - PHÒNG CSGT ĐẮK LẮK
Địa chỉ: Phòng CSGT - Tỉnh Đắk Lắk
Số điện thoại liên hệ: 02623.968359
2. Đội Cảnh sát giao thông, Trật tự - Công an thành phố Buôn Ma Thuột - Tỉnh Đắk Lắk
Địa chỉ: Thành phố Buôn Ma Thuột
```
+ Thực hiện quy trình tương tự đối với xe máy.
---
### 3 Ghi Chú:
+ OCR CAPTCHA Khồn thể chính sát được 100% nên mình cho thực 5 lần truy vấn.
---
# Cấu trúc thu mục:
```bash
├── Hinhanh    # thư Mục 
├── New folder # thư Mục 
├── phatnguoi.py         
├── requirements.txt     
└── README.md            
```

