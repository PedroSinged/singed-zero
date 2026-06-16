import machine
import ssd1306
import time
from wifi.scanner import executar_scan
from wifi.beacon import executar_beacon
from bluetooth.ble_scanner import executar_ble_scan

# Hardware
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

btn_cima = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
btn_baixo = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
btn_select = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

# Estado atual
estado_atual = "menu_principal"
menu_pos = 0

# Resultados do scan Wi-Fi
redes_24 = []
redes_5g = []
redes_pos = 0
origem_scan = "scan_24"

# Resultados do scan BLE
dispositivos_ble = []
ble_pos = 0

# Menus
menus = {
    "menu_principal": ["Wi-Fi", "Bluetooth", "Sub-GHz", "Configs"],
    "menu_wifi":      ["Scanner 2.4G", "Scanner 5G+", "Beacon Spam", "Deauth", "Voltar"],
    "menu_beacon":    ["Singed Mode", "Hacker Mode", "Random Mode", "Voltar"],
    "menu_bluetooth": ["BLE Scanner", "Voltar"],
}

navegacao = {
    "menu_principal": ["menu_wifi", "menu_bluetooth", None, None],
    "menu_wifi":      ["scan_24", "scan_5g", "menu_beacon", None, "menu_principal"],
    "menu_beacon":    ["beacon_singed", "beacon_hacker", "beacon_random", "menu_wifi"],
    "menu_bluetooth": ["ble_scan", "menu_principal"],
}

def desenhar_menu(itens, pos):
    oled.fill(0)
    inicio = (pos // 4) * 4
    for i, idx in enumerate(range(inicio, min(inicio + 4, len(itens)))):
        y = i * 16
        if idx == pos:
            oled.fill_rect(0, y, 128, 16, 1)
            oled.text("> " + itens[idx], 4, y + 4, 0)
        else:
            oled.text("  " + itens[idx], 4, y + 4, 1)
    oled.show()

def desenhar_lista_redes(redes, pos):
    oled.fill(0)
    if not redes:
        oled.text("Nenhuma rede", 10, 16)
        oled.text("encontrada.", 10, 32)
        oled.text("[select] voltar", 4, 50)
        oled.show()
        return

    inicio = (pos // 3) * 3
    for i, idx in enumerate(range(inicio, min(inicio + 3, len(redes)))):
        y = i * 20
        if y + 18 > 64:
            break
        rede = redes[idx]
        ssid = rede['ssid'][:12]
        rssi = str(rede['rssi'])

        if idx == pos:
            oled.fill_rect(0, y, 128, 18, 1)
            oled.text(ssid, 4, y + 2, 0)
            oled.text(rssi, 96, y + 2, 0)
        else:
            oled.text(ssid, 4, y + 2, 1)
            oled.text(rssi, 96, y + 2, 1)
    oled.show()

def desenhar_lista_ble(dispositivos, pos):
    oled.fill(0)
    if not dispositivos:
        oled.text("Nenhum disp.", 10, 16)
        oled.text("encontrado.", 10, 32)
        oled.text("[select] voltar", 4, 50)
        oled.show()
        return

    inicio = (pos // 3) * 3
    for i, idx in enumerate(range(inicio, min(inicio + 3, len(dispositivos)))):
        y = i * 20
        if y + 18 > 64:
            break
        disp = dispositivos[idx]
        nome = disp['nome'][:12]
        rssi = str(disp['rssi'])

        if idx == pos:
            oled.fill_rect(0, y, 128, 18, 1)
            oled.text(nome, 4, y + 2, 0)
            oled.text(rssi, 96, y + 2, 0)
        else:
            oled.text(nome, 4, y + 2, 1)
            oled.text(rssi, 96, y + 2, 1)
    oled.show()

def desenhar_detalhes_ble(disp):
    oled.fill(0)
    oled.text(disp['nome'][:16], 0, 0)
    oled.hline(0, 10, 128, 1)
    oled.text("MAC:", 0, 14)
    oled.text(disp['mac'][:17], 0, 24)
    oled.text("RSSI:", 0, 38)
    oled.text(str(disp['rssi']) + " dBm", 40, 38)
    oled.text("[any] voltar", 10, 54)
    oled.show()

def desenhar_detalhes(rede):
    seg = ["Open", "WEP", "WPA", "WPA2", "WPA/WPA2"]
    oled.fill(0)
    oled.text(rede['ssid'][:16], 0, 0)
    oled.hline(0, 10, 128, 1)
    oled.text("CH:" + str(rede['canal']), 0, 14)
    oled.text(str(rede['rssi']) + "dBm", 60, 14)
    oled.text(seg[rede['seguranca']] if rede['seguranca'] < len(seg) else "???", 0, 28)
    oled.text(rede['bssid'], 0, 42)
    oled.text(rede['faixa'], 0, 56)
    oled.show()

# Loop principal
desenhar_menu(menus[estado_atual], menu_pos)

while True:
    # Navegacao em menus
    if estado_atual in menus:
        itens = menus[estado_atual]

        if btn_cima.value() == 0:
            menu_pos = (menu_pos - 1) % len(itens)
            desenhar_menu(itens, menu_pos)
            time.sleep(0.2)

        if btn_baixo.value() == 0:
            menu_pos = (menu_pos + 1) % len(itens)
            desenhar_menu(itens, menu_pos)
            time.sleep(0.2)

        if btn_select.value() == 0:
            proximo = navegacao[estado_atual][menu_pos]
            if proximo in ("scan_24", "scan_5g"):
                redes_24, redes_5g = executar_scan(oled)
                origem_scan = proximo
                estado_atual = proximo
                redes_pos = 0
                redes = redes_24 if proximo == "scan_24" else redes_5g
                desenhar_lista_redes(redes, redes_pos)
            elif proximo in ("beacon_singed", "beacon_hacker", "beacon_random"):
                estado_atual = proximo
                modo = proximo.replace("beacon_", "")
                executar_beacon(oled, modo, btn_select)
                estado_atual = "menu_beacon"
                menu_pos = 0
                desenhar_menu(menus["menu_beacon"], menu_pos)
            elif proximo == "ble_scan":
                dispositivos_ble = executar_ble_scan(oled, btn_select)
                estado_atual = "lista_ble"
                ble_pos = 0
                desenhar_lista_ble(dispositivos_ble, ble_pos)
            elif proximo:
                estado_atual = proximo
                menu_pos = 0
                desenhar_menu(menus[estado_atual], menu_pos)
            time.sleep(0.3)

    # Navegacao na lista de redes Wi-Fi
    elif estado_atual in ("scan_24", "scan_5g"):
        redes = redes_24 if estado_atual == "scan_24" else redes_5g

        if btn_cima.value() == 0:
            if redes:
                redes_pos = (redes_pos - 1) % len(redes)
                desenhar_lista_redes(redes, redes_pos)
            time.sleep(0.2)

        if btn_baixo.value() == 0:
            if redes:
                redes_pos = (redes_pos + 1) % len(redes)
                desenhar_lista_redes(redes, redes_pos)
            time.sleep(0.2)

        if btn_select.value() == 0:
            if redes:
                estado_atual = "detalhes_rede"
                desenhar_detalhes(redes[redes_pos])
            else:
                estado_atual = "menu_wifi"
                menu_pos = 0
                desenhar_menu(menus["menu_wifi"], menu_pos)
            time.sleep(0.3)

    # Tela de detalhes Wi-Fi
    elif estado_atual == "detalhes_rede":
        if btn_select.value() == 0 or btn_cima.value() == 0 or btn_baixo.value() == 0:
            estado_atual = origem_scan
            redes = redes_24 if origem_scan == "scan_24" else redes_5g
            desenhar_lista_redes(redes, redes_pos)
            time.sleep(0.3)

    # Navegacao na lista BLE
    elif estado_atual == "lista_ble":
        if btn_cima.value() == 0:
            if dispositivos_ble:
                ble_pos = (ble_pos - 1) % len(dispositivos_ble)
                desenhar_lista_ble(dispositivos_ble, ble_pos)
            time.sleep(0.2)

        if btn_baixo.value() == 0:
            if dispositivos_ble:
                ble_pos = (ble_pos + 1) % len(dispositivos_ble)
                desenhar_lista_ble(dispositivos_ble, ble_pos)
            time.sleep(0.2)

        if btn_select.value() == 0:
            if dispositivos_ble:
                estado_atual = "detalhes_ble"
                desenhar_detalhes_ble(dispositivos_ble[ble_pos])
            else:
                estado_atual = "menu_bluetooth"
                menu_pos = 0
                desenhar_menu(menus["menu_bluetooth"], menu_pos)
            time.sleep(0.3)

    # Tela de detalhes BLE
    elif estado_atual == "detalhes_ble":
        if btn_select.value() == 0 or btn_cima.value() == 0 or btn_baixo.value() == 0:
            estado_atual = "lista_ble"
            desenhar_lista_ble(dispositivos_ble, ble_pos)
            time.sleep(0.3)