import machine
import ssd1306
import time

# Hardware
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

btn_cima = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
btn_baixo = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
btn_select = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

# Estado atual
estado_atual = "menu_principal"

# Menus
menus = {
    "menu_principal": ["Wi-Fi", "Bluetooth", "Sub-GHz", "Configs"],
    "menu_wifi":      ["Scanner", "Beacon Spam", "Deauth", "Voltar"],
    "menu_bt":        ["Scan BLE", "Voltar"],
}

# Mapa de navegação — select leva para qual estado?
navegacao = {
    "menu_principal": ["menu_wifi", "menu_bt", None, None],
    "menu_wifi":      [None, None, None, "menu_principal"],
    "menu_bt":        [None, "menu_principal"],
}

menu_pos = 0

def desenhar_menu(itens, pos):
    oled.fill(0)
    for i, item in enumerate(itens):
        y = i * 16
        if i == pos:
            oled.fill_rect(0, y, 128, 16, 1)
            oled.text("> " + item, 4, y + 4, 0)
        else:
            oled.text("  " + item, 4, y + 4, 1)
    oled.show()

# Loop principal
desenhar_menu(menus[estado_atual], menu_pos)

while True:
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
        if proximo:
            estado_atual = proximo
            menu_pos = 0
            desenhar_menu(menus[estado_atual], menu_pos)
        time.sleep(0.3)