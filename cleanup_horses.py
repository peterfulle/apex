#!/usr/bin/env python3
"""
Script para limpiar migraciones problemáticas de la aplicación horses
que no existe en el código actual pero tiene migraciones en la base de datos.
"""

import os
import sys
import django
from django.db import connection
from django.core.management import execute_from_command_line

def setup_django():
    """Configura Django para usar este script"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydevsite.settings')
    django.setup()

def cleanup_horses_migrations():
    """Elimina las migraciones problemáticas de horses"""
    print("🔄 Limpiando migraciones problemáticas de horses...")
    
    with connection.cursor() as cursor:
        try:
            # Verificar si la tabla django_migrations existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'django_migrations'
                );
            """)
            
            if not cursor.fetchone()[0]:
                print("❌ La tabla django_migrations no existe")
                return False
            
            # Eliminar las migraciones de horses de la tabla django_migrations
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'horses';
            """)
            
            deleted_count = cursor.rowcount
            print(f"✅ Eliminadas {deleted_count} migraciones de horses")
            
            # Intentar eliminar las tablas de horses si existen
            tables_to_drop = [
                'horses_horse',
                'horses_horse_internal_id_c019ac91_uniq',  # La constraint problemática
            ]
            
            for table in tables_to_drop:
                try:
                    # Verificar si la tabla existe
                    cursor.execute(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = '{table}'
                        );
                    """)
                    
                    if cursor.fetchone()[0]:
                        cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                        print(f"✅ Tabla {table} eliminada")
                    else:
                        print(f"ℹ️  Tabla {table} no existe")
                        
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {table}: {e}")
            
            # Intentar eliminar constraints que puedan estar sueltas
            try:
                cursor.execute("""
                    DROP INDEX IF EXISTS horses_horse_internal_id_c019ac91_uniq;
                """)
                print("✅ Constraint horses_horse_internal_id_c019ac91_uniq eliminada")
            except Exception as e:
                print(f"ℹ️  Constraint ya no existe: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al limpiar migraciones: {e}")
            return False

def main():
    """Función principal"""
    print("🚀 Iniciando limpieza de migraciones problemáticas...")
    
    setup_django()
    
    if cleanup_horses_migrations():
        print("✅ Limpieza completada exitosamente")
        print("🔄 Ahora ejecuta: python manage.py migrate")
    else:
        print("❌ Error en la limpieza")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
