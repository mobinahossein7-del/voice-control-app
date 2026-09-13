[app]

# اسم التطبيق
title = Voice Control App

# اسم الحزمة
package.name = voicecontrol

# نطاق الحزمة
package.domain = org.voice

# مجلد المشروع
source.dir = .

# الملفات التي سيتم تضمينها
source.include_exts = py,png,jpg,jpeg,kv,atlas

# إصدار التطبيق
version = 0.1

# المتطلبات
requirements = python3,kivy

# الصلاحيات
android.permissions = INTERNET,RECORD_AUDIO,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

# اتجاه الشاشة
orientation = portrait

# Android API
android.api = 36

# أقل إصدار Android مدعوم
android.minapi = 21

# إصدار NDK
android.ndk = 29

# قبول تراخيص Android تلقائياً
android.accept_sdk_license = True

# استخدام python-for-android الحديث المتوافق مع Python 3.14
p4a.branch = develop


[buildozer]

# مستوى السجل
log_level = 2

# تحذير التشغيل كمستخدم root
warn_on_root = 1
