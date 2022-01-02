# bash
Traffic count by iptables.log
Данные скрипты были написаны мной в 2010г. для мониторинга трафика через логи утилиты iptraf, которые имеют вид
Sun Jan  2 18:27:45 2022; TCP; eth1; 46 bytes; from 107.189.12.186:47486 to 188.168.202.228:8080; first packet (SYN)
Sun Jan  2 18:27:45 2022; TCP; eth1; 40 bytes; from 188.168.202.228:8080 to 107.189.12.186:47486; Connection reset; 1 packets, 40 bytes, avg flow rate 0.00 kbits/s; opposite direction 1 packets, 46 bytes; avg flow rate 0.00 kbits/s

iptraf_count считает общий внешний трафик по минутам в течение указанного десятка минут
iptraf_count_m считает трафик для указанного Ip и указаной минуты
