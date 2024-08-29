from src.routes.cpu_usage import cpu_usage_bp
from src.routes.disk_usage import disk_usage_bp
from src.routes.homepage import homepage_bp
from src.routes.memory_usage import memory_usage_bp
from src.routes.network_stats import network_stats_bp
from src.routes.settings import settings_bp
from src.routes.speedtest import speedtest_bp
from src.routes.system_health import system_health_bp

__all__ = [
    "cpu_usage_bp",
    "disk_usage_bp",
    "homepage_bp",
    "memory_usage_bp",
    "network_stats_bp",
    "settings_bp",
    "speedtest_bp",
    "system_health_bp",
]