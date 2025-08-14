#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"
#include "board_config.h"

// Thông tin Wi‑Fi
const char* ssid     = "3Tan";
const char* password = "3Sin/Cos";
// URL endpoint FastAPI (thay bằng địa chỉ server của bạn)
const char* serverUrl = "http://192.168.250.11:8000/upload-image/";

void setup() {
  Serial.begin(115200);
  // Kết nối Wi‑Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi connected!");

  // Khởi camera (ví dụ AI‑Thinker)
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_VGA;
  config.jpeg_quality = 12;
  config.fb_count     = 1;
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    while (true) { delay(1000); }
  }
}

void loop() {
  // 1. Chụp ảnh
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    return;
  }

  // 2. Gửi HTTP POST nếu Wi‑Fi OK
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "image/jpeg");
    int code = http.POST(fb->buf, fb->len);
    if (code > 0) {
      Serial.printf("HTTP POST… code: %d\n", code);
    } else {
      Serial.printf("HTTP failed, error: %s\n", http.errorToString(code).c_str());
    }
    http.end();
  }

  // 3. Trả buffer và đợi
  esp_camera_fb_return(fb);
  delay(10000); // gửi 1 tấm mỗi 10s (tuỳ bạn chỉnh)
}

