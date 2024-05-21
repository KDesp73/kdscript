#!/bin/bash

exe="kdscript"


if [ "$1" == "clean" ]; then
    sudo rm /usr/bin/$exe
    sudo rm /usr/share/man/man8/$exe.8.gz
    rm -r build
    rm -r dist
    rm *.spec

    echo "[INFO] Application uninstalled successfully"
    exit 0
fi

if [ -f "./dist/main" ]; then
    # Install the executable
    sudo cp ./dist/main /usr/bin/$exe
    if [ $? -ne 0 ]; then
        echo "[ERRO] Failed to copy the executable to /usr/bin/"
        exit 1
    fi
    echo "[INFO] $exe installed successfully"

    # Install man page
    sudo install -g 0 -o 0 -m 0644 $exe.man /usr/share/man/man8/$exe.8
    sudo gzip /usr/share/man/man8/$exe.8
    if [ $? -ne 0 ]; then
        echo "[ERRO] Failed to install man page"
        exit 1
    fi
    echo "[INFO] man page installed successfully"

    rm *.spec
    echo "[INFO] Installation completed successfully."
else
    echo "[WARN] $exe is not built. Building..."
    
    pyinstaller --onefile src/main.py

    if [[ $? == 0 ]]; then
        ./install.sh
    else
        echo "[ERRO] Failed to build $exe"
        exit 1
    fi
fi

exit 0
