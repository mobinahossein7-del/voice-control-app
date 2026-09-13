[app]

# (str) Title of your application
title = Voice Control App

# (str) Package name
package.name = voicecontrol

# (str) Package domain (needed for android packaging)
package.domain = org.voice

# (list) Source files to include (let it state .py and assets)
source.dir = .

# (list) Source files to include (let it state what to include)
source.exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# (str) Supported orientations
orientation = portrait

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android SDK build tools version
android.sdk_build_tools_version = 33.0.0

# (str) Android NDK version to use
android.ndk = 25b

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
