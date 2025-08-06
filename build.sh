#!/bin/bash

# Build script para Render
echo "🚀 Iniciando build para Render..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Aplicar migraciones
echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput

# Poblar datos iniciales (solo si es la primera vez)
echo "📊 Poblando datos iniciales de Aplyfly..."
python manage.py populate_aplyfly_data

echo "✅ Build completado exitosamente!"
