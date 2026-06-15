import network
import urandom
import time

SSIDS_SINGED = [
    "Do not chase Singed",
    "Singed WiFi",
    "Potion Seller",
    "I am the chemist",
    "Insanity Potion",
    "Fling me if u can",
    "Proxy King",
    "Mixed a new one",
    "Zyra was a mistake",
]

SSIDS_HACKER = [
    "FBI Surveillance Van",
    "NSA_Monitor_Unit_3",
    "Not A Bomb",
    "Definitely Not FBI",
    "HackTheWifi",
    "WarDriving_Active",
    "P4ck3t_Sn1ff3r",
    "Rede_Segura_Confie",
    "SkyNet_Node_7",
]

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"

def gerar_ssid_random():
    tamanho = urandom.randint(6, 16)
    return ''.join([urandom.choice(CHARS) for _ in range(tamanho)])

def executar_beacon(oled, modo, btn_select):
    # Garante que o AP começa desligado antes de religar
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    time.sleep(0.3)
    ap.active(True)

    if modo == "singed":
        lista = SSIDS_SINGED
    elif modo == "hacker":
        lista = SSIDS_HACKER
    else:
        lista = None

    idx = 0

    # Aguarda o botao ser solto antes de comecar
    while btn_select.value() == 0:
        time.sleep(0.05)
    time.sleep(0.2)

    while True:
        # Verifica botao
        if btn_select.value() == 0:
            while btn_select.value() == 0:
                time.sleep(0.05)
            time.sleep(0.2)
            break

        # Escolhe o SSID
        if lista:
            ssid = lista[idx % len(lista)]
            idx += 1
        else:
            ssid = gerar_ssid_random()

        # Configura o AP
        try:
            ap.config(essid=ssid, authmode=0)
        except:
            pass

        # Exibe na tela
        oled.fill(0)
        oled.text("BEACON SPAM", 20, 0)
        oled.hline(0, 10, 128, 1)
        oled.text(modo.upper(), 40, 14)
        oled.text(ssid[:16], 0, 32)
        if len(ssid) > 16:
            oled.text(ssid[16:], 0, 44)
        oled.text("[select] parar", 4, 54)
        oled.show()

        time.sleep(0.5)

    # Desliga o AP ao sair
    ap.active(False)
    time.sleep(0.2)