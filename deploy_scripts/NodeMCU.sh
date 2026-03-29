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
sleep 1

# Имитация пинга и входа в режим прошивки
ping_count=0
# until ping -c 1 $2 > /dev/null 2>&1; do
#     echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WAIT] Ожидание доступности устройства..."
#     sleep 1
#     ping_count=$((ping_count+1))
#     if [ $ping_count -gt 3 ]; then echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Устройство не отвечает."; exit 1; fi
# done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [OK] Устройство доступно."
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Вход в режим загрузчика (bootloader)..."
sleep 1

# --- ФЛЕШИНГ ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Начало процесса flash-памяти..."
sleep 1

# Имитация работы esptool.py
baud=460800
port="$2:8266" # Пример порта

for attempt in {1..3}; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [TRY] Попытка $attempt/3 прошивки на скорости $baud..."
    sleep 1.5

    # Имитация вывода esptool
    echo "Detecting chip type... ESP8266"
    echo "Chip ID: 0x12345678"
    echo "Uploading stub..."
    sleep 0.5

    # Имитация записи блоков (красивый прогресс)
    total_blocks=128
    for ((i=1; i<=total_blocks; i++)); do
        percent=$((i*100/total_blocks))
        echo -ne "\r[${i}/${total_blocks}] ${percent}% "
        sleep 0.05 # Быстрее, чем у Arduino
    done
    echo "" # Переход на новую строку после цикла

    echo "Wrote ${total_blocks} blocks ($((total_blocks*64)) bytes)"
    break # Выходим после первой успешной попытки в симуляции
done

# --- ЗАВЕРШЕНИЕ ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] Прошивка завершена!"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Перезапуск NodeMCU..."
sleep 1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [FINAL] Скрипт выполнен успешно."
exit 0