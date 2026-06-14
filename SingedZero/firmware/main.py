import machine
import ssd1306
import time
from wifi.scanner import executar_scan

# Hardware
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

btn_cima = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
btn_baixo = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
btn_select = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

# Estado atual
estado_atual = "menu_principal"
menu_pos = 0

# Resultados do scan
redes_24 = []
redes_5g = []
redes_pos = 0
origem_scan = "scan_24"  # guarda de qual scan viemos

# Menus
menus = {
    "menu_principal": ["Wi-Fi", "Bluetooth", "Sub-GHz", "Configs"],
    "menu_wifi":      ["Scanner 2.4G", "Scanner 5G+", "Beacon Spam", "Deauth", "Voltar"],
}

navegacao = {
    "menu_principal": ["menu_wifi", None, None, None],
    "menu_wifi":      ["scan_24", "scan_5g", None, None, "menu_principal"],
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
            elif proximo:
                estado_atual = proximo
                menu_pos = 0
                desenhar_menu(menus[estado_atual], menu_pos)
            time.sleep(0.3)

    # Navegacao na lista de redes
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
                # Tem redes: abre detalhes
                estado_atual = "detalhes_rede"
                desenhar_detalhes(redes[redes_pos])
            else:
                # Sem redes: volta ao menu_wifi
                estado_atual = "menu_wifi"
                menu_pos = 0
                desenhar_menu(menus["menu_wifi"], menu_pos)
            time.sleep(0.3)

    # Tela de detalhes
    elif estado_atual == "detalhes_rede":
        if btn_select.value() == 0 or btn_cima.value() == 0 or btn_baixo.value() == 0:
            # Volta para o scan de origem
            estado_atual = origem_scan
            redes = redes_24 if origem_scan == "scan_24" else redes_5g
            desenhar_lista_redes(redes, redes_pos)
            time.sleep(0.3)