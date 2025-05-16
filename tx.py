import serial
import struct
import time

# Mở cổng serial (tùy chỉnh COM port và baudrate theo nhu cầu)
ser = serial.Serial(port='COM4', baudrate=115200)

def gui_du_lieu(data1, data2):
    # Đảm bảo data là unsigned 16-bit
    data1 = max(0, min(data1, 0xFFFF))
    data2 = max(0, min(data2, 0xFFFF))

    # Gói dữ liệu: 0x02 + 2 byte data1 + 2 byte data2
    packet = struct.pack('>BHH', 0x02, data1, data2)  # '>': big-endian, B:1byte, H:2byte

    # Gửi qua UART
    ser.write(packet)
    print(f"Gửi: {packet.hex()}")

# Ví dụ gửi
while True:
    gui_du_lieu(403, 130)
    time.sleep(1)
