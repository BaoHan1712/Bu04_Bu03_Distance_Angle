import serial
import threading
import time

# Mở cổng serial (chỉnh COM cho đúng)
ser = serial.Serial('COM4', 115200, timeout=1)

def read_uart_loop():
    """Luồng đọc dữ liệu từ UART"""
    while True:
        data = ser.read(4)  # Đọc 4 byte: [0x11][D1][D2][0x12]
        if len(data) == 4:
            if data[0] == 0x11 and data[3] == 0x12:
                kc_distance = data[1] | (data[2] << 8)
                print(f"← Khoảng cách nhận: {kc_distance:.2f} mm")
            else:
                print(f"← Gói sai định dạng: {data.hex(' ').upper()}")
        elif len(data) > 0:
            print(f"← Dữ liệu không đủ 4 byte: {data.hex(' ').upper()}")

        time.sleep(0.05)  # Giảm tải CPU

def send_command_loop():
    """Luồng gửi byte 0x02 định kỳ mỗi 2 giây"""
    while True:
        ser.write(b'\x02')
        print("→ Đã gửi byte 0x02 yêu cầu khoảng cách.")
        time.sleep(1.0)

try:
    # Tạo và chạy hai luồng
    reader_thread = threading.Thread(target=read_uart_loop, daemon=True)
    sender_thread = threading.Thread(target=send_command_loop, daemon=True)

    reader_thread.start()
    sender_thread.start()

    # Giữ chương trình chạy
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nĐã dừng chương trình.")
finally:
    ser.close()
