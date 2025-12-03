# 🚀 Guía de Deployment en Render - Aplyfly

## 📋 Configuración de Web Service en Render

### 1. **Información Básica**
- **Name:** `aplyfly-site` (o el nombre que prefieras)
- **Language:** Python 3
- **Branch:** `main`
- **Region:** Oregon (US West) o la región que prefieras

### 2. **Comandos de Build y Start**
```bash
# Build Command:
./build.sh

# Start Command:
gunicorn mydevsite.wsgi:application
```

### 3. **Variables de Entorno Requeridas**

Agrega estas variables de entorno en Render:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.7` | Versión de Python |
| `SECRET_KEY` | `tu-clave-secreta-super-larga-y-segura` | Clave secreta de Django |
| `DEBUG` | `False` | Modo debug (debe ser False en producción) |
| `DATABASE_URL` | *(se genera automáticamente)* | URL de PostgreSQL |

#### 🔐 Generar SECRET_KEY
Usa este comando para generar una clave secreta segura:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. **Base de Datos PostgreSQL**

1. En el dashboard de Render, ve a **"New"** → **"PostgreSQL"**
2. Configura:
   - **Name:** `aplyfly-db`
   - **Database:** `aplyfly`
   - **User:** `aplyfly_user`
   - **Region:** Misma región que tu web service
3. Una vez creada, conecta la base de datos:
   - Ve a tu Web Service → **"Environment"**
   - Agrega la variable: `DATABASE_URL` con el valor de la BD PostgreSQL

### 5. **Proceso de Deployment**

El script `build.sh` ejecutará automáticamente:
```bash
1. 📦 Instalar dependencias (pip install -r requirements.txt)
2. 📁 Recopilar archivos estáticos (collectstatic)
3. 🗄️ Aplicar migraciones (migrate)
4. 📊 Poblar datos iniciales de Aplyfly
```

### 6. **Configuración de Instancia**

#### Para Desarrollo/Testing:
- **Instance Type:** Free ($0/mes)
- **RAM:** 512 MB
- **CPU:** 0.1

#### Para Producción:
- **Instance Type:** Starter ($7/mes) o superior
- **RAM:** 512 MB+
- **CPU:** 0.5+

### 7. **Verificación Post-Deployment**

Una vez desplegado, verifica:

1. ✅ **Sitio accesible:** https://tu-app.onrender.com
2. ✅ **Formulario de contacto funcional:** Prueba enviar un mensaje
3. ✅ **Admin panel:** https://tu-app.onrender.com/admin
4. ✅ **Datos poblados:** Servicios, proyectos y testimonios visibles

### 8. **Crear Superusuario en Producción**

Usa el shell de Render para crear un superusuario:

```bash
# En el shell de Render:
python manage.py createsuperuser
```

### 9. **Dominios Personalizados (Opcional)**

Para usar un dominio personalizado:
1. Ve a **"Settings"** → **"Custom Domains"**
2. Agrega tu dominio
3. Configura los registros DNS según las instrucciones

### 🎯 **URLs Importantes**

- **Sitio Principal:** https://tu-app.onrender.com
- **Panel Admin:** https://tu-app.onrender.com/admin
- **Contacto:** https://tu-app.onrender.com/contacto/
- **Servicios:** https://tu-app.onrender.com/servicios/

### 🔧 **Troubleshooting**

#### Error de Build:
- Verifica que `build.sh` tenga permisos de ejecución
- Revisa los logs de build en Render

#### Error de Database:
- Confirma que `DATABASE_URL` esté configurado
- Verifica conexión a PostgreSQL

#### Error 500:
- Revisa `DEBUG=False` en producción
- Verifica `SECRET_KEY` esté configurado
- Revisa logs de la aplicación

### 📊 **Monitoreo**

Render provee métricas automáticas:
- CPU/RAM usage
- Response times
- Error rates
- Request volume

---

## 🎉 ¡Listo!

Tu sitio de Aplyfly estará funcionando en: **https://tu-app.onrender.com**

Con todas las funcionalidades:
- 🏢 Identidad corporativa Aplyfly
- 🌙 Tema oscuro profesional
- 💻 Simulador de código Python
- 📝 Formulario de contacto funcional
- 📊 Datos de ejemplo poblados
- 🗄️ Base de datos persistente
