# 🎮 Roblox AutoRejoin Tool

Tool tự động vào lại game Roblox khi bị disconnect hoặc crash. Chạy 24/7 trên Cloud Phone (UGPhone, VSPhone, etc.)

## ✨ Tính năng

- ✅ Tự động phát hiện khi Roblox crash hoặc disconnect
- ✅ Tự động vào lại game bằng deep link
- ✅ Chạy 24/7 trên cloud phone
- ✅ Logging chi tiết với màu sắc
- ✅ Thống kê rejoin success rate
- ✅ Screenshot khi có lỗi (optional)
- ✅ Retry logic thông minh

## 📋 Yêu cầu

- Android device hoặc Cloud Phone (UGPhone, VSPhone, etc.)
- **ROOT access** (bắt buộc)
- Termux app
- Roblox app đã cài đặt
- Python 3.x

## 🚀 Cài đặt

### Bước 1: Cài đặt Termux

1. Tải Termux từ F-Droid hoặc GitHub
2. Mở Termux

### Bước 2: Root Termux

```bash
# Cấp quyền root cho Termux
su
```

### Bước 3: Chạy Setup Script

```bash
# Download và chạy setup
curl -O https://raw.githubusercontent.com/VNDevorE/AutoRejoinhehe/main/setup.sh
bash setup.sh
```

Hoặc nếu đã có source code:

```bash
cd /sdcard/Download/AutoRejoin
bash setup.sh
```

### Bước 4: Cấu hình (Optional)

Chỉnh sửa `config.json` nếu cần:

```json
{
  "game_id": "1554960397",
  "check_interval": 30,
  "max_retries": 5,
  "retry_delay": 10,
  "roblox_package": "com.roblox.client"
}
```

## 🎯 Sử dụng

### Chạy tool

```bash
# Cách 1: Dùng run script
bash run.sh

# Cách 2: Chạy trực tiếp
su -c "cd /sdcard/Download/AutoRejoin && python autorejoin.py"

# Cách 3: Chạy trong background
nohup bash run.sh > /dev/null 2>&1 &
```

### Dừng tool

Nhấn `Ctrl + C` để dừng

## 📊 Giao diện

Tool sẽ hiển thị:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🎮  ROBLOX AUTO-REJOIN TOOL  🎮                   ║
║                                                           ║
║        Tự động vào lại game khi bị disconnect            ║
║        Chạy 24/7 trên Cloud Phone                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

📋 Loading configuration...
✓ Game ID: 1554960397
✓ Check Interval: 30s
✓ Max Retries: 5

[09:00:00] [INFO] State changed: None → in_game
[09:00:30] [INFO] State: in_game
[09:01:00] [WARNING] ⚠️  Disconnected from game!
[09:01:00] [INFO] 🔄 Attempting to rejoin...
[09:01:15] [SUCCESS] ✓ Successfully rejoined!
```

## 🔧 Cấu trúc thư mục

```
AutoRejoin/
├── autorejoin.py          # Main script
├── config.json            # Cấu hình
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── run.sh                # Run script
├── modules/              # Core modules
│   ├── __init__.py
│   ├── adb_helper.py     # ADB wrapper
│   ├── detector.py       # State detection
│   ├── launcher.py       # Game launcher
│   ├── logger.py         # Logging
│   ├── monitor.py        # Main monitor
│   └── screenshot.py     # Screenshot manager
└── logs/                 # Log files
    ├── screenshots/      # Error screenshots
    └── YYYYMMDD.log      # Daily logs
```

## 🛠️ Troubleshooting

### Tool không chạy

1. Kiểm tra ROOT access: `su` trong Termux
2. Kiểm tra Python: `python --version`
3. Kiểm tra ADB: `which adb` hoặc `pidof com.roblox.client`

### Không tự động join được

1. Kiểm tra Game ID trong `config.json`
2. Thử join manual bằng deep link:
   ```bash
   am start -a android.intent.action.VIEW -d "roblox://placeId=1554960397"
   ```
3. Kiểm tra log trong `logs/`

### Roblox bị crash liên tục

1. Tăng `retry_delay` trong config
2. Kiểm tra RAM của cloud phone
3. Restart cloud phone

## 📝 Lưu ý

- Tool này chỉ dành cho mục đích cá nhân, không thương mại
- Cần ROOT access để hoạt động
- Chạy tốt nhất trên cloud phone đã root sẵn
- Có thể cần điều chỉnh selectors nếu Roblox update UI

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Tạo issue hoặc pull request.

## 📄 License

MIT License - Free to use for personal purposes

## 🙏 Credits

Made with ❤️ for Roblox players who want to AFK 24/7

---

**⚠️ Disclaimer**: Tool này chỉ tự động hóa việc vào lại game khi bị disconnect. Không phải hack, không vi phạm ToS của Roblox.
