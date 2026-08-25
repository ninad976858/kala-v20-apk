[app]
title = KALA Vishwaroopam V20
package.name = kalavishwaroopam
package.domain = org.kala
source.dir = .
source.include_exts = py,json,jsonl
source.include_patterns = *.py,*.jsonl,*.json,evidence/*
version = 20.0
requirements = python3
orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
