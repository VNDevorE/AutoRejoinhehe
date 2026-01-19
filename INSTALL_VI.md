# 📱 Hướng dẫn cài đặt chi tiết

## 🎯 Chuẩn bị

### Những gì bạn cần:

1. **Cloud Phone** (UGPhone, VSPhone, LDPlayer, etc.) hoặc Android device thật
2. **Roblox app** đã cài đặt
3. **Termux app** - Tải từ [F-Droid](https://f-droid.org/packages/com.termux/)
4. **ROOT access** - Hầu hết cloud phone đã root sẵn

## 📖 Các bước cài đặt

### Bước 1: Cài đặt Termux

#### Trên Cloud Phone (UGPhone/VSPhone):

1. Mở Play Store hoặc browser
2. Tải Termux từ F-Droid: https://f-droid.org/packages/com.termux/
3. Cài đặt Termux

#### Trên Android thật:

1. Tải Termux từ F-Droid (KHÔNG tải từ Play Store - phiên bản cũ)
2. Cài đặt

### Bước 2: Mở Termux lần đầu

1. Mở app Termux
2. Chờ nó tự động setup (khoảng 30 giây)
3. Bạn sẽ thấy dấu nhắc lệnh: `$`

### Bước 3: Cấp quyền ROOT

```bash
# Gõ lệnh này và nhấn Enter
su
```

- Nếu có popup xin quyền ROOT → Chọn **Allow/Cho phép**
- Dấu nhắc sẽ đổi từ `$` thành `#`
- Nếu báo lỗi "su: not found" → Cloud phone chưa root, liên hệ support

### Bước 4: Cấp quyền truy cập Storage

```bash
# Thoát root trước
exit

# Cấp quyền storage
termux-setup-storage
```

- Popup xin quyền → Chọn **Allow/Cho phép**

### Bước 5: Update Termux

```bash
# Thay đổi repository (nếu cần)
termux-change-repo

# Chọn mirror gần nhất (thường là Mirrors by BFSU)
# Nhấn Space để chọn, Enter để OK

```bash
pkg update -y && pkg upgrade -y && pkg install python git android-tools -y
```
#### Cách 1: Từ GitHub (NÊN DÙNG)

Nên cài vào thư mục gốc của Termux để tránh lỗi quyền (`Permission denied`):

```bash
# cài colormar
pip install colorama

# Clone code
git clone https://github.com/VNDevorE/AutoRejoinhehe.git

# Vào thư mục
cd AutoRejoinhehe
```

### Bước 11: Chạy tool lần đầu

Nên chạy bằng lệnh này để đảm bảo quyền root nhận diện đúng Python:

Hoặc nếu bạn đã gõ `su` trước đó (dấu `#`):
```bash
PATH=$PATH python autorejoin.py
```

## ✅ Kiểm tra hoạt động

Tool sẽ hiển thị:

```
╔═══════════════════════════════════════════════════════════╗
║        🎮  ROBLOX AUTO-REJOIN TOOL  🎮                   ║
╚═══════════════════════════════════════════════════════════╝

📋 Loading configuration...
✓ Game ID: 1554960397
✓ Check Interval: 30s
✓ Max Retries: 5

[09:00:00] [INFO] Initial state: loading
[09:00:05] [INFO] Starting initial game join...
[09:00:10] [SUCCESS] ✓ Successfully joined game!
```

## 🔄 Chạy tool 24/7

### Cách 1: Chạy trong background

```bash
# Chạy background với nohup
nohup bash run.sh > /dev/null 2>&1 &

# Kiểm tra process
ps aux | grep autorejoin
```

### Cách 2: Dùng screen (khuyên dùng)

```bash
# Cài screen
pkg install screen -y

# Tạo session mới
screen -S autorejoin

# Chạy tool
bash run.sh

# Thoát screen (tool vẫn chạy): Nhấn Ctrl+A, sau đó D

# Quay lại screen:
screen -r autorejoin
```

### Cách 3: Dùng Termux:Boot (auto-start khi khởi động)

```bash
# Cài Termux:Boot từ F-Droid
# Tạo script boot

mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-autorejoin.sh
```

Nội dung file:

```bash
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
su -c "cd /sdcard/Download/AutoRejoin && python autorejoin.py" &
```

Lưu và cấp quyền:

```bash
chmod +x ~/.termux/boot/start-autorejoin.sh
```

## 🛑 Dừng tool

### Nếu chạy foreground:
Nhấn `Ctrl + C`

### Nếu chạy background:
```bash
# Tìm process ID
ps aux | grep autorejoin

# Kill process
kill -9 [PID]
```

### Nếu dùng screen:
```bash
screen -r autorejoin
# Sau đó nhấn Ctrl+C
```

### Lỗi 6: Máy không thể Root (Non-Root)

**Triệu chứng**: Chạy tool báo lỗi `Permission denied` hoặc không thể thực hiện các thao tác `tap`, `swipe`.

**Giải thích**: Tool cần quyền Root để điều khiển một app khác (Roblox). Nếu không có Root, Termux bị chặn không cho can thiệp vào app ngoài.

**Giải pháp (Dành cho máy thật)**:
1.  Bật **Developer Options** (Tùy chọn nhà phát triển) trên điện thoại.
2.  Bật **Wireless Debugging** (Gỡ lỗi không dây).
3.  Cài đặt `android-tools` trong Termux: `pkg install android-tools`.
4.  Dùng lệnh `adb connect` để kết nối Termux với chính nó (localhost).
5.  Khi đã kết nối ADB thành công, tool có thể chạy thông qua ADB shell mà không cần Root.

**Lưu ý cho Cloud Phone**:
Hầu hết Cloud Phone (UGPhone, VSPhone) đều có mục cài đặt để **Bật Root**. Bạn hãy kiểm tra trong phần cài đặt của máy cloud đó. Nếu cloud phone hoàn toàn không cho Root, tool này hiện tại **chưa hỗ trợ** hoàn hảo.

### Lỗi 2: "python: command not found"

**Nguyên nhân**: Python chưa cài đặt

**Giải pháp**:
```bash
pkg install python -y
```

### Lỗi 3: "No module named 'colorama'"

**Nguyên nhân**: Thiếu dependencies

**Giải pháp**:
```bash
pip install colorama
```

### Lỗi 4: Tool không tự động join game

**Nguyên nhân**: 
- Roblox chưa cài đặt
- Game ID sai
- Không có quyền root

**Giải pháp**:
1. Kiểm tra Roblox đã cài chưa
2. Thử join manual:
```bash
su -c "am start -a android.intent.action.VIEW -d 'roblox://placeId=1554960397'"
```
3. Kiểm tra log trong `logs/`

### Lỗi 5: "Permission denied"

**Nguyên nhân**: Chưa cấp quyền execute

**Giải pháp**:
```bash
chmod +x setup.sh run.sh
```

## 📊 Xem logs

```bash
# Xem log hôm nay
cat logs/$(date +%Y%m%d).log

# Xem log real-time
tail -f logs/$(date +%Y%m%d).log

# Xem screenshots lỗi
ls -lh logs/screenshots/
```

## 💡 Tips & Tricks

### 1. Giảm CPU usage

Tăng `check_interval` trong config:

```json
{
  "check_interval": 60
}
```

### 2. Tắt screenshot để tiết kiệm dung lượng

```json
{
  "screenshot_on_error": false
}
```

### 3. Chạy nhiều game cùng lúc

Tạo nhiều folder với config khác nhau:

```bash
cp -r AutoRejoin AutoRejoin_Game2
cd AutoRejoin_Game2
nano config.json  # Đổi game_id
```

## 🎓 Kiến thức thêm

### Cách tool hoạt động:

1. **Monitor**: Kiểm tra trạng thái Roblox mỗi 30s
2. **Detect**: Phát hiện crash/disconnect qua process và UI
3. **Rejoin**: Dùng deep link `roblox://placeId=XXX` để join lại
4. **Retry**: Tự động retry nếu fail, có backoff logic

### Deep Link là gì?

Deep link là URL đặc biệt mở trực tiếp app:
```
roblox://placeId=1554960397
```

Khi mở link này, Android sẽ:
1. Mở Roblox app
2. Tự động join vào game ID 1554960397

## 📞 Hỗ trợ

Nếu gặp vấn đề:

1. Kiểm tra logs trong `logs/`
2. Chụp screenshot lỗi
3. Tạo issue trên GitHub
4. Hoặc liên hệ qua Zalo/Telegram

---

**Chúc bạn AFK thành công! 🎮**
