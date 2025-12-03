#!/usr/bin/env python
"""
Script para arreglar problemas de migraciones en producción
Ejecutar en el servidor de Render
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def fix_migration_issues():
    """Arregla problemas comunes de migraciones en producción"""
    print("🔧 Arreglando problemas de migraciones...")
    
    with connection.cursor() as cursor:
        try:
            # 1. Limpiar migraciones problemáticas de horses (que no existe)
            print("🧹 Limpiando migraciones de horses...")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'horses';")
            print("✅ Migraciones de horses eliminadas")
            
            # 2. Marcar migraciones básicas como aplicadas si no existen
            print("📋 Verificando migraciones básicas...")
            
            # Verificar migraciones de clients
            cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'clients';")
            clients_count = cursor.fetchone()[0]
            
            if clients_count == 0:
                print("📝 Marcando migraciones de clients como aplicadas...")
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('clients', '0001_initial', NOW())
                """)
            
            # 3. Resetear migraciones conflictivas
            print("🔄 Reseteando migraciones conflictivas...")
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'admin' AND name = '0001_initial'
                AND id NOT IN (
                    SELECT MIN(id) FROM django_migrations 
                    WHERE app = 'admin' AND name = '0001_initial'
                )
            """)
            
            print("✅ Problemas de migraciones corregidos")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def run_migrations():
    """Ejecuta las migraciones después del fix"""
    print("🚀 Ejecutando migraciones...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        print("✅ Migraciones ejecutadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        return False

if __name__ == "__main__":
    print("🔧 SCRIPT DE REPARACIÓN DE MIGRACIONES - RENDER")
    print("=" * 50)
    
    if fix_migration_issues():
        if run_migrations():
            print("🎉 ¡Todas las migraciones reparadas exitosamente!")
        else:
            print("⚠️ Migraciones parcialmente reparadas")
    else:
        print("❌ Error en la reparación")
        sys.exit(1)
