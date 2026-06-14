import network
import time

def executar_scan(oled):
    # Ativa o Wi-Fi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    # Loading animado
    pontos = ["Scanneando.", "Scanneando..", "Scanneando..."]
    for i in range(6):
        oled.fill(0)
        oled.text(pontos[i % 3], 10, 28)
        oled.show()
        time.sleep(0.4)
    
    # Executa o scan
    redes = wifi.scan()
    
    # Processa os resultados
    redes_24 = []
    redes_5g = []
    
    for rede in redes:
        ssid = rede[0].decode('utf-8') if rede[0] else '<Oculta>'
        bssid = ':'.join(['%02x' % b for b in rede[1]])
        canal = rede[2]
        rssi = rede[3]
        seguranca = rede[4]
        faixa = "2.4G" if canal <= 13 else "5G+"
        
        dados = {
            "ssid": ssid,
            "bssid": bssid,
            "canal": canal,
            "rssi": rssi,
            "seguranca": seguranca,
            "faixa": faixa
        }
        
        if faixa == "2.4G":
            redes_24.append(dados)
        else:
            redes_5g.append(dados)
    
    # Ordena por sinal (mais forte primeiro)
    redes_24.sort(key=lambda x: x['rssi'], reverse=True)
    redes_5g.sort(key=lambda x: x['rssi'], reverse=True)
    
    return redes_24, redes_5g