# Hệ Thống Phát Hiện Buồn Ngủ (Drowsiness Detection System)

<div align="center">
  <img src="/api/placeholder/800/200" alt="Drowsiness Detection System Banner">
  <p><strong>An intelligent system for monitoring driver drowsiness using computer vision</strong></p>
</div>

## 📋 Mục Lục

- [Tổng Quan](#tổng-quan)
- [Tính Năng](#tính-năng)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Cách Sử Dụng](#cách-sử-dụng)
- [Nguyên Lý Hoạt Động](#nguyên-lý-hoạt-động)
- [Cấu Hình Tham Số](#cấu-hình-tham-số)
- [Phím Tắt](#phím-tắt)
- [Ghi Log](#ghi-log)
- [Giải Quyết Vấn Đề](#giải-quyết-vấn-đề)
- [Đóng Góp](#đóng-góp)
- [Giấy Phép](#giấy-phép)

## 🔍 Tổng Quan

Hệ thống phát hiện buồn ngủ là một ứng dụng sử dụng thị giác máy tính và học máy để phát hiện trạng thái buồn ngủ của người lái xe. Hệ thống liên tục theo dõi các dấu hiệu buồn ngủ như nhắm mắt kéo dài và ngáp, giúp cảnh báo người dùng để tránh các tai nạn do ngủ gật gây ra.

<div align="center">
  <img src="/api/placeholder/640/360" alt="Drowsiness Detection Demo">
</div>

## ✨ Tính Năng

- **Theo dõi thời gian nhắm mắt**: Phát hiện khi người lái xe nhắm mắt quá lâu
- **Phát hiện ngáp**: Nhận biết khi người lái xe ngáp, một dấu hiệu của mệt mỏi
- **Cảnh báo âm thanh**: Phát âm thanh cảnh báo khi phát hiện trạng thái buồn ngủ
- **Ghi log hoạt động**: Lưu lại các sự kiện để phân tích sau này
- **Hiển thị trực quan**: Giao diện trực quan hiển thị các chỉ số và cảnh báo
- **Theo dõi khuôn mặt liên tục**: Thuật toán theo dõi giúp duy trì việc phát hiện ngay cả khi có chuyển động
- **Điều chỉnh các ngưỡng**: Cho phép tinh chỉnh độ nhạy của hệ thống dễ dàng

## 💻 Yêu Cầu Hệ Thống

| Thành phần | Yêu cầu tối thiểu |
|------------|-------------------|
| Hệ điều hành | Windows (đã hỗ trợ), Linux/Mac (cần sửa đổi phần cảnh báo âm thanh) |
| CPU | 2.0 GHz dual-core |
| RAM | 4GB |
| Webcam | Camera có độ phân giải tối thiểu 640x480 |
| Python | 3.6 trở lên |

## 📦 Cài Đặt

### 1. Cài đặt các gói phụ thuộc

```bash
pip install opencv-python dlib numpy scipy argparse
```

### 2. Tải file mô hình dlib

Tải xuống file `shape_predictor_68_face_landmarks.dat` từ trang web của dlib hoặc repository chính thức:

```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
```

### 3. Kiểm tra cài đặt

Đảm bảo tất cả các thư viện đã được cài đặt đúng và file shape predictor được đặt trong cùng thư mục với script hoặc được chỉ định đường dẫn trong tham số.

## 🚀 Cách Sử Dụng

### Chạy với cấu hình mặc định:

```bash
python drowsiness_detector.py
```

### Chạy với các tùy chọn:

```bash
python drowsiness_detector.py --shape-predictor path/to/shape_predictor_68_face_landmarks.dat --ear-threshold 0.25 --ear-frames 20 --yawn-threshold 0.6 --alarm --show-landmarks --log drowsiness_log.txt
```

## 🔧 Nguyên Lý Hoạt Động

### Kiến trúc tổng quan

<div align="center">
  <img src="/api/placeholder/700/300" alt="System Architecture">
</div>

### Quy trình xử lý

1. **Thu nhận hình ảnh**: Lấy khung hình từ webcam
2. **Phát hiện khuôn mặt**: Sử dụng dlib để xác định vị trí khuôn mặt
3. **Trích xuất facial landmark**: Xác định 68 điểm đặc trưng trên khuôn mặt
4. **Tính toán các chỉ số**:
   - Eye Aspect Ratio (EAR): Đo mức độ nhắm/mở mắt
   - Mouth Ratio (MR): Đo mức độ mở miệng
5. **Đưa ra quyết định**: So sánh với các ngưỡng và đếm số frame liên tiếp
6. **Phát cảnh báo**: Kích hoạt cảnh báo nếu vượt ngưỡng

### Công thức tính toán

#### Eye Aspect Ratio (EAR)

EAR được tính dựa trên khoảng cách giữa các điểm facial landmark của mắt:

<div align="center">
  <img src="/api/placeholder/400/150" alt="EAR Formula">
</div>

```
EAR = (||p₂-p₆|| + ||p₃-p₅||) / (2 * ||p₁-p₄||)
```

Trong đó pᵢ là các điểm facial landmark của mắt.

#### Mouth Ratio (MR)

MR được tính dựa trên tỷ lệ giữa chiều cao và chiều rộng của miệng:

```
MR = ||p₁₃-p₁₉|| / ||p₀-p₆||
```

## ⚙️ Cấu Hình Tham Số

| Tham số | Mô tả | Giá trị mặc định |
|---------|-------|-----------------|
| `--shape-predictor` | Đường dẫn đến file dlib facial landmark predictor | `shape_predictor_68_face_landmarks.dat` |
| `--ear-threshold` | Ngưỡng EAR để phát hiện mắt nhắm | 0.25 |
| `--ear-frames` | Số frame liên tiếp với EAR dưới ngưỡng để kích hoạt cảnh báo | 20 |
| `--yawn-threshold` | Ngưỡng tỷ lệ miệng để phát hiện ngáp | 0.6 |
| `--camera` | Chỉ số camera | 0 |
| `--show-landmarks` | Hiển thị facial landmarks | False |
| `--alarm` | Bật cảnh báo âm thanh | False |
| `--log` | Đường dẫn đến file log | None |
| `--face-tracking` | Bật tính năng theo dõi khuôn mặt liên tục | True |

## ⌨️ Phím Tắt

| Phím | Chức năng |
|------|-----------|
| `ESC` | Thoát chương trình |
| `r` | Reset bộ đếm |
| `+` | Tăng ngưỡng EAR |
| `-` | Giảm ngưỡng EAR |

## 📝 Ghi Log

Khi bật tính năng ghi log, hệ thống sẽ lưu lại các sự kiện quan trọng vào file văn bản:

- Thời điểm bắt đầu phiên
- Các thông số cấu hình
- Thời điểm phát hiện ngáp
- Thời điểm phát cảnh báo buồn ngủ

Ví dụ nội dung log:

```
==================================================
Phiên phát hiện buồn ngủ bắt đầu lúc 2025-05-09 15:30:45
Ngưỡng EAR: 0.25, Khung hình: 20, Ngưỡng ngáp: 0.6
==================================================

[2025-05-09 15:31:22] Phát hiện ngáp lần thứ 1
[2025-05-09 15:32:45] CẢNH BÁO: Phát hiện buồn ngủ
[2025-05-09 15:35:10] Phát hiện ngáp lần thứ 2
```

## 🔍 Giải Quyết Vấn Đề

| Vấn đề | Giải pháp |
|--------|-----------|
| Không phát hiện được khuôn mặt | - Kiểm tra ánh sáng<br>- Điều chỉnh vị trí camera<br>- Đảm bảo khuôn mặt nằm trong khung hình |
| Sai lệch trong phát hiện mắt nhắm | - Điều chỉnh `--ear-threshold`<br>- Tăng giá trị cho người có mắt nhỏ hơn<br>- Giảm giá trị cho người có mắt to hơn |
| Cảnh báo không kích hoạt | - Kiểm tra `--ear-frames`<br>- Đảm bảo `--alarm` được bật |
| Hiệu suất chậm | - Giảm độ phân giải camera<br>- Đảm bảo phần cứng đáp ứng yêu cầu tối thiểu |
| Lỗi âm thanh | - Đối với Linux/Mac, cần thay thế module `winsound` bằng giải pháp tương ứng |

## 👥 Đóng Góp

Đóng góp cho dự án luôn được chào đón! Nếu bạn muốn tham gia:

1. Fork repository
2. Tạo nhánh cho tính năng mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi của bạn (`git commit -m 'Add some amazing feature'`)
4. Push lên nhánh (`git push origin feature/amazing-feature`)
5. Mở Pull Request

### Hướng phát triển tiếp theo

- [ ] Hỗ trợ đa nền tảng cho cảnh báo âm thanh
- [ ] Thêm khả năng phát hiện nghiêng đầu
- [ ] Cải thiện việc theo dõi khuôn mặt trong điều kiện ánh sáng yếu
- [ ] Phát triển giao diện người dùng đồ họa
- [ ] Tích hợp thông báo qua thiết bị di động

## 📄 Giấy Phép

Dự án được phân phối dưới giấy phép MIT. Xem thêm tại tệp `LICENSE`.
