#!/bin/bash

# Activar entorno virtual y ejecutar script de población
source /Users/peterfulle/Desktop/apex-main/venv/bin/activate
cd /Users/peterfulle/Desktop/apex-main
python manage.py shell < populate_blog.py
