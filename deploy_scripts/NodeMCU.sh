#!/usr/bin/env bash

# nodemcu.sh - Скрипт деплоя для NodeMCU (ESP8266) по Wi-Fi/SPI
# Аргументы: $1 - Путь к файлу с кодом, $2 - IP-адрес устройства

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Запуск скрипта деплоя для NodeMCU"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Целевой IP: $2"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Подготовка бинарного файла..."
sleep 1

# Имитация конвертации в бинарник для ESP
if [ ! -f "$1" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Файл с кодом не найден!"
    exit 1
fi

output_bin="firmware.bin"
cp "$1" "$output_bin" # Просто копируем для имитации конвертации
chmod +x "$output_bin"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [OK] Бинарный файл $output_bin создан."

# --- ПОДКЛЮЧЕНИЕ К ESP ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Попытка подключения к ESP8266 по адресу $2..."
sleep 2

# Имитация пинга и входа в режим прошивки
ping_count=0
until ping -c 1 $2 > /dev/null 2>&1; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WAIT] Ожидание доступности устройства..."
    sleep 1
    ping_count=$((ping_count+1))
    if [ $ping_count -gt 5 ]; then echo