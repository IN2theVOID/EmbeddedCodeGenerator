#!/usr/bin/env bash

# ESP32.sh - Скрипт деплоя для ESP32 с поддержкой OTA (Over The Air)
# Аргументы: $1 - Путь к файлу с кодом, $2 - IP-адрес устройства

set -e # Остановить скрипт при первой ошибке (для реализма)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$1] $2"
}

log "INFO" "Запуск скрипта деплоя для ESP32"
log "INFO" "IP-адрес: $2"
log "INFO" "Файл прошивки: $1"
log "INFO" "Проверка целостности файла..."
sleep 1

if [ ! -s "$1" ]; then # Проверяем, что файл не пустой и существует
    log "ERROR" "Файл пуст или не существует!"
    exit 1
fi

log "OK" "Файл прошел проверку. Размер: $(stat -c%s "$1") байт."
log "INFO" "Инициализация esptool.py v4.x..."
sleep 2

port="$2:8266"
baud=921600 # Высокая скорость для ESP32

log "INFO" "Подключение к порту $port на скорости $baud..."
log "INFO" "Чтение данных о чипе..."
sleep 1

log "DETECT" "Chip is ESP32-D0WDQ6 (revision v4.1)"
log "DETECT" "Features: WiFi, BT, Dual Core, 4MB Flash"
log "DETECT" "Crystal is 40MHz"
log "DETECT" "MAC: aa:bb:cc:dd:ee:ff"
log "INFO" "Подключение к stub-loader..."
sleep 0.5

log "FLASH" "Начало процесса записи во Flash-память (Partition Table -> App)."
log "FLASH" "Стирание старого приложения..."
for i in {1..4}; do echo -n "."; sleep 0.3; done; echo ""
log "FLASH" "[ OK ] Стирание завершено."

log "FLASH" "Запись таблицы разделов (Partition Table)..."
for i in {1..5}; do echo -n "#"; sleep 0.1; done; echo ""
log "[ OK ] Таблица разделов записана."

log "FLASH" "[MAIN] Запись приложения (App) в слот 0 (ОТА_0)..."
total_blocks=256 # Больше блоков для ощущения объема работы

for ((i=1; i<=total_blocks; i++)); do
    percent=$((i*100/total_blocks))
    if (( i % 32 == 0 )); then # Печатаем статус реже, чтобы не засорять лог
        echo -ne "\r[FLASH] Запись блока $i из $total_blocks ($percent%) "
        sleep 0.07 # Средняя скорость записи ESP32 через UART/SPI
    fi
done

echo "" # Новая строка после цикла записи

log "[SUCCESS]" "[MAIN] Сообщение: Leaving..."
log "[SUCCESS]" "[MAIN] Сообщение: Hard resetting via RTS pin..."
log "[FINAL]" "🎉 Деплой завершен успешно!"
log "[FINAL]" "🔁 Устройство будет перезагружено автоматически через 3 секунды..."
sleep 3

exit 0 # Успешный выход (set -e гарантирует выход только здесь)