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

### Bước 12: Thiết lập game (Interactive Setup)

Khi chạy lần đầu, tool sẽ hỏi bạn:

```
============================================================
🎮  THIẾT LẬP GAME
============================================================

❓ Bạn có VIP server không? (Y/N):
```

#### Nếu bạn có VIP Server (chọn Y):

```
❓ Bạn có VIP server không? (Y/N): Y

📋 Dán link VIP server vào đây:
   (Ví dụ: https://ro.blox.com/... hoặc https://www.roblox.com/share?code=...)
👉 Link: [paste link của bạn]

✅ Đã lưu VIP server link!
💾 Đã lưu cấu hình vào game_config.json
```

#### Nếu không có VIP Server (chọn N):

```
❓ Bạn có VIP server không? (Y/N): N

📋 Nhập Game ID:
   (Ví dụ: 1554960397)
👉 Game ID: 1554960397

✅ Đã lưu Game ID: 1554960397
💾 Đã lưu cấu hình vào game_config.json
```

> **💡 Lưu ý quan trọng:**
> - File `game_config.json` được tạo **LOCAL** trên cloud phone của bạn
> - **KHÔNG** cần push lên Git
> - Mỗi cloud phone có thể chạy game khác nhau
> - Muốn đổi game? Xóa `game_config.json` và chạy lại tool!

### Bước 13: Đổi game (nếu cần)

Để chuyển sang game khác:

```bash
# Xóa config cũ
rm game_config.json

# Chạy lại tool, nó sẽ hỏi setup game mới
PATH=$PATH python autorejoin.py
```

## ✅ Kiểm tra hoạt động

Tool sẽ hiển thị:

```
╔═══════════════════════════════════════════════════════════╗
║        🎮  ROBLOX AUTO-REJOIN TOOL  🎮                   ║
╚═══════════════════════════════════════════════════════════╝

📋 Loading configuration...
✓ VIP Server: Đã cấu hình
✓ Check Interval: 30s
✓ Max Retries: 5

[09:00:00] [INFO] Initial state: loading
[09:00:05] [INFO] Starting initial game join...
[09:00:10] [SUCCESS] ✓ Successfully joined game!
```

## 🔄 Quản lý nhiều game

**Tình huống:** Bạn có 5 cloud phone, mỗi phone chạy 1 game khác nhau

**Giải pháp:**
1. Clone repo trên tất cả cloud phone
2. Mỗi phone chạy `python autorejoin.py`
3. Nhập game ID hoặc VIP link riêng cho từng phone
4. Mỗi phone có `game_config.json` riêng → Không conflict!

**Ưu điểm:**
- ✅ Không cần edit code
- ✅ Không cần push Git mỗi lần đổi game
- ✅ Setup nhanh chóng
- ✅ Dễ quản lý
