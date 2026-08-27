from app.utils.constants import (
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
)


class CriticalDeviceService:

    @staticmethod
    def get_critical_reasons(device):
        reasons = []

        cpu = float(device.cpu_usage or 0)
        memory = float(device.memory_usage or 0)
        disk = float(device.disk_usage or 0)

        cpu_threshold = CPU_THRESHOLD
        memory_threshold = MEMORY_THRESHOLD
        disk_threshold = DISK_THRESHOLD

        if cpu >= cpu_threshold:
            reasons.append(
                {
                    "type": "CPU",
                    "label": "CPU High",
                    "value": cpu,
                    "threshold": cpu_threshold,
                }
            )

        if memory >= memory_threshold:
            reasons.append(
                {
                    "type": "MEMORY",
                    "label": "Memory High",
                    "value": memory,
                    "threshold": memory_threshold,
                }
            )

        if disk >= disk_threshold:
            reasons.append(
                {
                    "type": "DISK",
                    "label": "Disk High",
                    "value": disk,
                    "threshold": disk_threshold,
                }
            )

        if device.status and device.status.upper() == "OFFLINE":
            reasons.append(
                {
                    "type": "STATUS",
                    "label": "Device Offline",
                    "value": None,
                    "threshold": None,
                }
            )

        return reasons
