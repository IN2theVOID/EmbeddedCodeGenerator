from abc import ABC
import subprocess

from modules.database import DbGenerations, DbDevice
from modules.exceptions import DeployError
from modules.logger import log, LoggerDecorator

class Deploy(ABC):
    def deploy(self, devices: list, generation: str):
        ...

class DeployToDevice(Deploy):
    @LoggerDecorator()
    def deploy(self, devices, generation):
        try:
            # Список для сбора результатов выполнения каждого скрипта
            deployment_results = []
            genInfo = DbGenerations()
            deviceInfo = DbDevice()
            code = genInfo.get_info(generation)[0][1]
            log.info(code)
            for device in devices:
                log.info(deviceInfo.get_info(device))
                label = deviceInfo.get_info(device)[0][0]
                ip = deviceInfo.get_info(device)[0][1]
                type = deviceInfo.get_info(device)[0][2]
                log.info("Start deploy to: " + label + " " + ip + " " + type)

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