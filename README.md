# 🕵️‍♂️ Conan Discord Bot (Adugaywa Cỏ Nan)

Một con bot Discord giải trí và tương tác thông minh được xây dựng bằng ngôn ngữ **Python** (`discord.py`). Bot sử dụng API từ **OpenRouter** để trò chuyện với hai nhân cách linh hoạt (Conan Edogawa & Kudo Shinichi) cùng khả năng tạo ảnh nghệ thuật thông qua API của Pollinations.

---

## ✨ Tính Năng Nổi Bật

* **🤖 Nhân cách kép (Dual Personality):** 
  * Mặc định bot sẽ là **Conan Edogawa** hồn nhiên, dễ thương, thích dùng từ "Ủa, á lệ lệ?" kèm nhiều emoji tinh nghịch.
  * Khi phát hiện các từ khóa liên quan đến Tổ chức Áo đen hoặc tên thật (ví dụ: *shinichi, áo đen, gin, vodka, aptx 4869...*), bot sẽ lập tức biến hình thành **Kudo Shinichi** lạnh lùng, sắc bén để phá án.
* **🧠 Trí nhớ ngắn hạn (Memory System):** Lưu giữ bối cảnh của 10 câu thoại gần nhất cho từng người dùng để cuộc trò chuyện diễn ra tự nhiên, liền mạch.
* **💬 Tự động chat (Auto-chat Channel):** Cho phép thiết lập kênh riêng để bot tự động phản hồi mà không cần phải tag tên `@bot`.
* **🎨 Vẽ tranh AI (Image Generation):** Tích hợp lệnh vẽ ảnh siêu tốc theo mô tả bằng tiếng Việt.

---

## 🛠️ Danh Sách Lệnh (Commands)

| Lệnh | Chức năng |
| :--- | :--- |
| `!help` | Hiển thị bảng hướng dẫn sử dụng bot |
| `!setchannel` | Kích hoạt chế độ tự động trả lời (không cần tag) tại kênh hiện tại |
| `!stop` | Tắt chế độ tự động trả lời tại kênh hiện tại |
| `!xoa` | Xóa sạch ký ức trò chuyện giữa bạn và bot |
| `!ve [nội dung]` | Yêu cầu bot vẽ tranh theo mô tả (Ví dụ: `!ve con mèo mặc áo thám tử`) |

---

## 🚀 Hướng Dẫn Cài Đặt & Triển Khai

### 1. Yêu Cầu Hệ Thống
* Python 3.8 trở lên.
* Token của Discord Bot (Tạo từ Discord Developer Portal).
* API Key từ OpenRouter.

### 2. Cài Đặt Thư Viện
Mở Terminal/Command Prompt tại thư mục chứa bot và chạy lệnh sau để cài đặt các gói thư viện cần thiết:
```bash
pip install discord.py aiohttp python-dotenv
```

### 3. Cấu Hình File Môi Trường (`.env`)
Tạo một file có tên `.env` nằm cùng thư mục với file `bot.py` và nhập thông tin mã bảo mật của bạn:
```env
DISCORD_TOKEN=Nhập_Token_Bot_Discord_Của_Bạn_Tại_Đây
AI_API_KEY=Nhập_API_Key_OpenRouter_Của_Bạn_Tại_Đây
```

### 4. Cấu Hình File Cài Đặt (`config.json`)
Tạo file `config.json` để thiết lập tiền tố lệnh, model AI và các từ khóa kích hoạt nhân cách Shinichi:
```json
{
  "prefix": "!",
  "ai_model": "nex-agi/nex-n2-pro:free",
  "shinichi_triggers": [
    "áo đen", "black organization", "aptx 4869", "gin", "vodka", 
    "vermouth", "shinichi", "tổ chức", "thuốc teo nhỏ", "bo"
  ]
}
```

### 5. Khởi Chạy Bot
Chạy lệnh sau để đưa thám tử lừng danh lên sóng:
```bash
python bot.py
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
├── bot.py             # Mã nguồn chính điều khiển hoạt động của bot
├── config.json        # File cấu hình model AI và từ khóa hệ thống
├── .env               # Lưu trữ Token Discord và API Key (Bảo mật)
├── channels.json      # Danh sách ID các kênh được cấp quyền auto-chat
└── README.md          # Tài liệu hướng dẫn sử dụng dự án này
```

---

## 📜 Bản Quyền & Phát Triển
* **Phát triển bởi:** Karos (@imkaros)
* **Bản quyền thuộc về:** Karos
* Dự án được xây dựng với mục đích học tập giải trí, mã nguồn mở hoàn toàn công khai.

## ✨ Giao Lưu & Giải Trí
* Đội ngũ Supporters tận tình hỗ trợ mọi lúc.
* Bot độc quyền Ai Là Gián Điệp
* Giveaway xịn xò
* Tham gia Cộng Đồng Việt ngay [Tham Gia](https://discord.gg/Gju793PgHT) 