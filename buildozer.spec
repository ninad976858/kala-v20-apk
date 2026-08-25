[app]
title = KALA VISHWAROOPAM V20
package.name = kalavishwaroopam
package.domain = com.kala.vishwaroopam
source.dir =.
source.include_patterns = app/*,data/*,*.py,*.json,*.jsonl,*.md,*.txt,*.spec
version = 20.0
requirements = python3,kivy,requests,urllib3,charset-normalizer,certifi
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.build_tools_version = 33.0.2
android.accept_sdk_license_agreement = True
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
p4a.bootstrap = sdl2
p4a.local_recipes =
