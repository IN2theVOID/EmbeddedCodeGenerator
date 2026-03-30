from abc import ABC
from ast import List
from modules.database import Info
import subprocess

from modules.exceptions import DeployError

class Deploy(ABC):
    def deploy(self, devices: List, generation: str):
        ...

class DeployToDevice(Deploy):
    def deploy(self, devices, generation):
        try:
            # Список для сбора результатов выполнения каждого скрипта
            deployment_results = []
            info = Info()
            code = info.getGenerationDataByTask(generation)[0][1]
            print(code)
            for device in devices:
                print(info.getDeviceDataByLabel(device))
                label = info.getDeviceDataByLabel(device)[0][0]
                ip = info.getDeviceDataByLabel(device)[0][1]
                type = info.getDeviceDataByLabel(device)[0][2]
                print("Start deploy to: " + label + " " + ip + " " + type)

                with open("code.txt", "w") as file:
                    file.write(code)

                script = "deploy_scripts/" + type + ".sh"
                result = subprocess.run([script, "code.txt", ip], capture_output=True, text=True)
                device_result = {
                    "label": label,
                    "ip": ip,
                    "type": type,
                    "returncode": result.returncode, # Код возврата (0 - успех)
                    "stdout": result.stdout,         # Стандартный вывод (логи скрипта)
                    "stderr": result.stderr          # Ошибки (если есть)
                }
                
                deployment_results.append(device_result)
        except:
            raise DeployError

        return deployment_results