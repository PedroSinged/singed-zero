# Singed Zero

> A Flipper Zero-inspired multi-tool for wireless security research, built from scratch with ESP32 and MicroPython.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Platform](https://img.shields.io/badge/platform-ESP32-blue)
![Language](https://img.shields.io/badge/linguagem-MicroPython-green)

## Sobre o Projeto

O Singed Zero é um dispositivo de segurança ofensiva portátil inspirado no Flipper Zero, desenvolvido do zero com hardware acessível e documentado publicamente para fins educacionais.

## Hardware

| Componente | Especificação |
|------------|---------------|
| Microcontrolador | ESP32 WROOM DevKit |
| Display | OLED 0.96" 128x64 (SSD1306 I2C) |
| Interface | 3 botões (cima, baixo, select) |

## Funcionalidades

- [x] Menu navegável com state machine
- [x] Wi-Fi — Scanner
- [x] Wi-Fi — Beacon Spam (Singed Mode, Hacker Mode, Random Mode)
- [ ] Wi-Fi — Deauth
- [x] Bluetooth — BLE Scanner
- [ ] Bluetooth — BLE Spam (Apple/Android)
- [ ] Sub-GHz — CC1101 (planejado)
- [ ] NFC — (planejado)
- [ ] Infravermelho — (planejado)
- [ ] RFID — (em estudo)

## Estrutura do Projeto

singed-zero/

├── SingedZero/

│   ├── firmware/

│   │   ├── main.py

│   │   ├── oled/

│   │   ├── wifi/

│   │   └── bluetooth/

│   └── pymakr.conf

└── README.md

## Progresso

### v0.1 — Base do sistema
- Firmware MicroPython gravado no ESP32
- Display OLED inicializado via I2C
- Menu principal navegável com 3 botões
- State machine implementada para navegação entre submenus

### v0.2 — Wi-Fi Scanner
- Scanner de redes 2.4GHz e 5GHz
- Listagem com SSID e RSSI ordenados por sinal
- Tela de detalhes por rede (canal, BSSID, segurança, faixa)
- Paginação automática na lista de redes
- Loading animado durante o scan

### v0.3 — Beacon Spam
- Três modos: Singed Mode, Hacker Mode e Random Mode
- SSIDs temáticos e geração aleatória
- Loading animado e exibição do SSID atual no OLED
- Parada e retorno ao menu via botão select

### v0.4 — BLE Scanner
- Scanner de dispositivos BLE próximos
- Exibe nome, MAC e RSSI de cada dispositivo
- Paginação automática na lista
- Tela de detalhes por dispositivo

## Autor

**Pedro Trindade** — [@PedroSinged](https://github.com/PedroSinged)  
[LinkedIn](https://www.linkedin.com/in/pedro-trindade-118282244/)