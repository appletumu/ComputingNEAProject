from recallr.window import WindowManager
from recallr.objects import AppSettings

app_settings = AppSettings()

window = WindowManager(app_settings.app_name)

window.startup()