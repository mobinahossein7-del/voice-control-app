[app]

title = Voice Control App
package.name = voicecontrol
package.domain = org.voice

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

android.permissions = INTERNET,RECORD_AUDIO,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

orientation = portrait

android.api = 33
android.minapi = 21
android.sdk = 33
android.sdk_build_tools_version = 33.0.0
android.ndk = 25b

[buildozer]

log_level = 2
warn_on_root = 1
