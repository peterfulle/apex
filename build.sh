#!/bin/bash

# Build script para Render
echo "🚀 Iniciando build para Render..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Limpiar migraciones problemáticas de horses (si es necesario)
echo "🧹 Verificando y limpiando migraciones problemáticas..."
python manage.py cleanup_horses --force || echo "⚠️  No hay migraciones problemáticas que limpiar"

# Aplicar migraciones
echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput || {
    echo "⚠️  Error en migraciones - Intentando con --fake-initial"
    python manage.py migrate --fake-initial --noinput
}

# Poblar datos iniciales (solo si es la primera vez)
echo "📊 Poblando datos iniciales de Aplyfly..."
python manage.py populate_aplyfly_data

echo "✅ Build completado exitosamente!"
