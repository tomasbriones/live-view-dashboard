#!/bin/bash
if [ $# -eq 0 ]
    then echo "Debes indicar la variable de ambiente"
else
    echo "Instalando requirements.txt"
    pip3 install -r requirements.txt
    echo "Requirements instalado"

    echo "seteando variables de entorno:"
    . ./credentials/.env

    ENVIRONMENT=$1
    echo "seteando variable de entorno pasada en parametro:" $ENVIRONMENT
    export ENVIRONMENT=$1

    echo "Actuales variables de entorno:"
    env 

    echo "Ejecutando main.py"
    python3 main.py
fi