from abc import ABC
from ast import List
from modules.database import Info
import subprocess

class Deploy(ABC):
    def deploy(self, devices: List, generation: str):
        ...

class DeployToDevice(Deploy):
    def deploy(self, devices, generation):
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

            subprocess.run([script, "code.txt"])

        return True