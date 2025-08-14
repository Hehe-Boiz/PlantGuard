# test_backend.py
import requests
import os

# --- CẤU HÌNH TEST ---

# SERVER_URL = "http://0.0.0.0:8000/detect/evaluate"
SERVER_URL = "http://0.0.0.0:8000/detect/image"
IMAGE_PATH = "/home/heheboiz/data/bacterial-leaf-spot.jpeg" # 👈 THAY ĐỔI ĐƯỜNG DẪN NÀY

# --- HÀM GỬI YÊU CẦU ---

def send_test_image(image_path: str):
    """
    Đọc một file ảnh và gửi dữ liệu thô của nó đến server FastAPI.
    """
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file ảnh tại '{image_path}'")
        return

    print(f"Đang gửi ảnh '{os.path.basename(image_path)}' đến server...")

    try:
        # Đọc toàn bộ file ảnh vào bộ nhớ dưới dạng bytes
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Thiết lập header để server biết đây là dữ liệu ảnh jpeg
        # Điều này rất quan trọng, khớp với những gì ESP32 gửi
        headers = {
            "Content-Type": "image/jpeg"
        }

        # Gửi yêu cầu POST với dữ liệu ảnh thô trong body (dùng tham số `data`)
        response = requests.post(SERVER_URL, data=image_data, headers=headers, timeout=30)

        # Xử lý phản hồi từ server
        if response.status_code == 200:
            print("Thành công! Phản hồi từ server:")
            print(response.json())
        else:
            print(f"Thất bại! Mã trạng thái: {response.status_code}")
            print(f"   Nội dung lỗi: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối đến server: {e}")

if __name__ == "__main__":
    send_test_image(IMAGE_PATH)