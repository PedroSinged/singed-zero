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
- [ ] Wi-Fi — Scanner, Beacon Spam, Deauth
- [ ] Bluetooth — BLE Scanner
- [ ] Sub-GHz — CC1101 (planejado)

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

## Autor

**Pedro Trindade** — [@PedroSinged](https://github.com/PedroSinged)  
[LinkedIn](https://www.linkedin.com/in/pedro-trindade-118282244/)