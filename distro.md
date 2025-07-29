
# MacOS

pyinstaller --name 'ESP Flasher' \
            --icon './icon.ico' \
            --windowed  \
            --add-data='./icon.png:.' \
            --add-data='./logo.png:.' \
            --hidden-import='esptool.py' \
            esp_flasher.py\

create-dmg \
  --volname "ESP Flasher" \
  --volicon "icon.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "ESP Flasher.app" 175 120 \
  --hide-extension "ESP Flasher.app" \
  --app-drop-link 425 120 \
  "dist/ESP Flasher.dmg" \
  "dist/dmg/"

# Linux

# Windows