# 🌱 Dự án **Plant Guard**

> Hệ thống giám sát & điều khiển cây trồng sử dụng cảm biến IoT, phân tích AI và bảng điều khiển Web realtime.

## 1. Mục tiêu

- **Theo dõi**: thu thập dữ liệu độ ẩm đất, nhiệt độ, ánh sáng, v.v.
- **Phân tích**: Nhận biết xem cây hiện tại đang khỏe hay bệnh.
- **Điều khiển**: bơm, phun sương, cảnh báo sớm qua dashboard & push‑notification.

## 2. Cấu trúc thư mục (hiện tại)

```
edge/     # Firmware & suy luận tại thiết bị (Raspberry Pi/ESP32)
backend/  # API, rule‑engine, database & websocket
web/      # Dashboard React hiển thị realtime
ml/       # Notebook, pipeline huấn luyện & convert model
```

## 4. Quy tắc đóng góp

1. **Nhánh**: tạo branch `feature/<tên>` hoặc `bugfix/<tên>`.
2. **Commit**: theo [Conventional Commits](https://www.conventionalcommits.org/) – ví dụ `feat(edge): add soil sensor driver`.
3. **Pull Request**: kèm mô tả, screenshot nếu UI.

> Cập nhật README khi thêm module mới hoặc thay đổi cấu trúc thư mục.

