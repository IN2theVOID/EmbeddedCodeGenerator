static_form = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Генератор кода для встраиваемых систем</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .form-container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
            margin-bottom: 25px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        select, input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            box-sizing: border-box;
        }
        select:focus, input[type="text"]:focus {
            outline: none;
            border-color: #4CAF50;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        .info {
            margin-top: 20px;
            padding: 10px;
            background-color: #e7f3fe;
            border-left: 4px solid #2196F3;
            font-size: 13px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>🔧 Генератор кода</h2>
        
        <form action="http://127.0.0.1:8000/emb_code_gen" method="GET" target="_blank">
            
            <div class="form-group">
                <label for="language">Язык программирования:</label>
                <select name="language" id="language" required>
                    <option value="">-- Выберите язык --</option>
                    <option value="c++">C++</option>
                    <option value="c">C</option>
                    <option value="python">Python</option>
                    <option value="rust">Rust</option>
                    <option value="assembly">Assembly</option>
                    <option value="lua">Lua</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="platform">Платформа:</label>
                <select name="platform" id="platform" required>
                    <option value="">-- Выберите платформу --</option>
                    <option value="arm">ARM</option>
                    <option value="x86">x86</option>
                    <option value="x86_64">x86_64</option>
                    <option value="riscv">RISC-V</option>
                    <option value="avr">AVR</option>
                    <option value="esp32">ESP32</option>
                    <option value="nodemcu">NodeMCU</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="task">Задача (task):</label>
                <input 
                    type="text" 
                    name="task" 
                    id="task" 
                    placeholder="Например: hellowrld" 
                    required
                    title="Введите название задачи"
                >
            </div>
            
            <button type="submit">🚀 Сгенерировать код</button>
            
        </form>
        
        <div class="info">
            <strong>ℹ️ Примечание:</strong> 
            Форма отправляет GET-запрос на локальный сервер 
            <code>127.0.0.1:8000</code>. Убедитесь, что сервис запущен.
        </div>
    </div>

    <script>
        // Опционально: валидация перед отправкой
        document.querySelector('form').addEventListener('submit', function(e) {
            const language = document.getElementById('language').value;
            const platform = document.getElementById('platform').value;
            const task = document.getElementById('task').value.trim();
            
            if (!language || !platform || !task) {
                e.preventDefault();
                alert('Пожалуйста, заполните все поля формы');
                return false;
            }
            
            // Показываем формируемый URL в консоли для отладки
            const url = new URL(this.action);
            url.searchParams.append('language', language);
            url.searchParams.append('platform', platform);
            url.searchParams.append('task', task);
            console.log('🔗 Запрос:', url.toString());
        });
    </script>
</body>
</html>
'''