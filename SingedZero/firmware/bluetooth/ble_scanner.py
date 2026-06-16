import ubluetooth
import time

# Eventos BLE
_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6

dispositivos = {}

def executar_ble_scan(oled, btn_select):
    ble = ubluetooth.BLE()
    ble.active(True)

    # Aguarda botao ser solto antes de comecar
    while btn_select.value() == 0:
        time.sleep(0.05)
    time.sleep(0.2)

    # Limpa dispositivos anteriores
    dispositivos.clear()

    def callback(evento, dados):
        if evento == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = dados
            mac = ':'.join(['%02x' % b for b in bytes(addr)])
            nome = _extrair_nome(adv_data)
            dispositivos[mac] = {
                'mac': mac,
                'nome': nome if nome else '<Desconhecido>',
                'rssi': rssi
            }

    ble.irq(callback)
    ble.gap_scan(0, 30000, 30000, False)

    while True:
        if btn_select.value() == 0:
            while btn_select.value() == 0:
                time.sleep(0.05)
            time.sleep(0.2)
            break

        # Atualiza contagem na tela
        oled.fill(0)
        oled.text("BLE Scanner", 20, 0)
        oled.hline(0, 10, 128, 1)
        oled.text("Dispositivos:", 0, 16)
        oled.text(str(len(dispositivos)), 100, 16)
        oled.text("Scanneando...", 10, 32)
        oled.text("[select] parar", 4, 54)
        oled.show()
        time.sleep(0.5)

    ble.gap_scan(None)
    ble.active(False)
    return list(dispositivos.values())

def _extrair_nome(adv_data):
    i = 0
    while i < len(adv_data):
        length = adv_data[i]
        if length == 0:
            break
        tipo = adv_data[i + 1]
        if tipo in (0x08, 0x09):
            return bytes(adv_data[i + 2:i + 1 + length]).decode('utf-8', 'ignore')
        i += 1 + length
    return None