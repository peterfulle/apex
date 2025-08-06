# 🚀 Configuración de Render para Aplyfly

## 📋 Variables de Entorno Requeridas

Agrega estas variables en la sección **Environment** de tu servicio en Render:

### Variables Principales
```
DATABASE_URL=<URL_DE_POSTGRESQL>
SECRET_KEY=<TU_SECRET_KEY_SEGURA>
DEBUG=False
ALLOWED_HOSTS=equisalud.onrender.com,aplyfly.onrender.com
DJANGO_SETTINGS_MODULE=mydevsite.settings
```

### Variables de Email (Opcionales)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=info@aplyfly.com
```

## 🗄️ Base de Datos PostgreSQL

### Opción 1: PostgreSQL en Render (Recomendado)
1. En tu dashboard de Render, crea un nuevo **PostgreSQL Database**
2. Copia la **Internal Database URL** 
3. Agrégala como variable `DATABASE_URL` en tu web service

### Opción 2: PostgreSQL Externa
- **ElephantSQL** (gratuito hasta 20MB)
- **Supabase** (gratuito hasta 500MB)
- **Railway** (gratuito con limitaciones)

## ⚙️ Configuración del Servicio

### Build Command
```bash
./build.sh
```

### Start Command
```bash
gunicorn mydevsite.wsgi:application
```

### Variables de Entorno Específicas
- **ROOT_DIRECTORY**: Dejar vacío
- **AUTO_DEPLOY**: On Commit (recomendado)
- **BRANCH**: main

## 🔐 Usuario Admin Inicial

El script creará automáticamente un usuario admin:
- **Usuario**: admin
- **Email**: admin@aplyfly.com  
- **Contraseña**: admin123

⚠️ **IMPORTANTE**: Cambia la contraseña después del primer login.

## 📊 Datos Iniciales

El comando `populate_aplyfly_data` creará:
- ✅ 6 servicios de Aplyfly
- ✅ 3 proyectos destacados
- ✅ 3 testimonios de clientes
- ✅ Categorías y tecnologías

## 🔄 Flujo de Deploy

1. **Primera vez**: Se crea toda la estructura y datos
2. **Deploys posteriores**: Solo se actualizan migraciones y código
3. **Los datos persisten** entre deploys gracias a PostgreSQL

## 🐛 Troubleshooting

### Error de Base de Datos
- Verifica que `DATABASE_URL` esté configurada
- Asegúrate de que la BD PostgreSQL esté accesible

### Error de Migraciones
- Los datos existentes se mantienen
- Solo se aplican nuevas migraciones

### Error de Archivos Estáticos
- Verifica que WhiteNoise esté configurado
- Los archivos se recopilan en cada build

## 📝 Comandos Útiles

```bash
# Ejecutar localmente con PostgreSQL
python manage.py migrate
python manage.py populate_aplyfly_data
python manage.py runserver

# Crear superusuario adicional
python manage.py createsuperuser

# Ver estado de migraciones
python manage.py showmigrations
```

## 🔄 Backup de Datos

Para hacer backup de la BD PostgreSQL desde Render:
1. Ir a tu PostgreSQL database en Render
2. Usar la sección **Backups** 
3. O exportar manualmente con pg_dump

---

**¡Tu aplicación Aplyfly estará lista para producción!** 🎉
