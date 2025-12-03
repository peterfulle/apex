# 🚀 Guía de Deployment en Render - Aplyfly

## 📋 Pre-requisitos

1. Cuenta en [Render.com](https://render.com)
2. Repositorio Git (GitHub, GitLab, o Bitbucket)
3. Python 3.9+ instalado localmente

## 🔧 Preparación del Proyecto

### 1. Variables de Entorno Requeridas

En el dashboard de Render, configura estas variables de entorno:

#### **Obligatorias:**
```
SECRET_KEY=<genera-una-key-segura-aqui>
DEBUG=False
PYTHON_VERSION=3.9.10
```

#### **Opcionales (Email):**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

#### **Opcionales (Azure OpenAI para chat):**
```
AZURE_OPENAI_API_KEY=tu-key
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 2. Generar SECRET_KEY

Ejecuta en tu terminal local:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 Deployment en Render

### Opción A: Desde Dashboard (Recomendado)

1. **Crear Web Service:**
   - Ve a [Render Dashboard](https://dashboard.render.com/)
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio Git
   - Configura:
     - **Name:** `aplyfly` (o el que prefieras)
     - **Region:** Oregon (o el más cercano)
     - **Branch:** `main`
     - **Runtime:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn mydevsite.wsgi:application`
     - **Plan:** Free (o el que prefieras)

2. **Crear PostgreSQL Database:**
   - En Dashboard → "New +" → "PostgreSQL"
   - **Name:** `aplyfly-db`
   - **Region:** Same as web service
   - **Plan:** Free
   - Copia la **Internal Database URL**

3. **Configurar Variables de Entorno:**
   - En tu Web Service → "Environment"
   - Agrega todas las variables mencionadas arriba
   - **Importante:** Agrega `DATABASE_URL` con la URL interna de tu base de datos

4. **Deploy:**
   - Click en "Manual Deploy" → "Deploy latest commit"
   - Espera a que termine el build (5-10 minutos primera vez)

### Opción B: Usando render.yaml (Infraestructura como Código)

1. El archivo `render.yaml` ya está configurado en el proyecto
2. En Render Dashboard → "New +" → "Blueprint"
3. Conecta tu repositorio
4. Render detectará automáticamente `render.yaml`
5. Click "Apply" y espera el deployment

## 🎯 Post-Deployment

### 1. Crear Superusuario Admin

Desde el dashboard de Render, ve a tu Web Service → "Shell" y ejecuta:

```bash
python manage.py createsuperuser
```

O usa el que se crea automáticamente:
- **Email:** `prfulle@gmail.com`
- **Password:** `Carolina22.`

### 2. Verificar el Sitio

Tu aplicación estará disponible en:
```
https://tu-app-name.onrender.com
```

**URLs importantes:**
- **Home:** `/`
- **Panel Cliente:** `/clients/login/`
- **Panel Admin:** `/administrador/login/`
- **Django Admin:** `/admin/`

### 3. Datos Iniciales

El script `build.sh` ya ejecuta `populate_aplyfly_data` que crea:
- ✅ Categorías de proyectos
- ✅ Servicios
- ✅ Testimonios
- ✅ Proyectos de portafolio

## 🔒 Seguridad

### Configuraciones Automáticas en Producción:

Cuando `DEBUG=False`, el settings.py automáticamente activa:
- ✅ WhiteNoise para archivos estáticos
- ✅ ALLOWED_HOSTS configurado
- ✅ Compresión de archivos estáticos
- ✅ HTTPS enforcement (en Render)

### Recomendaciones:

1. **Nunca** subas tu archivo `.env` a Git
2. Mantén `SECRET_KEY` segura y única
3. Usa variables de entorno para credenciales
4. Configura email para notificaciones de errores

## 🛠️ Troubleshooting

### Error: "No module named 'psycopg'"
```bash
# Ya está incluido en requirements.txt
psycopg[binary]==3.2.4
```

### Error: "Static files not found"
```bash
# En Render Shell:
python manage.py collectstatic --noinput
```

### Error en Migraciones
```bash
# En Render Shell:
python manage.py migrate --fake-initial
```

### Ver Logs
En Render Dashboard → Tu Web Service → "Logs"

## 📊 Monitoreo

### Health Check
Render automáticamente hace health checks en `/`

### Logs en Tiempo Real
```bash
# En tu terminal local con Render CLI:
render logs -f
```

## 🔄 Actualizaciones

Para actualizar tu app después del deployment inicial:

1. **Git Push:**
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```

2. **Auto-Deploy:**
   - Render detecta el push y redeploy automáticamente
   - O puedes hacer "Manual Deploy" desde el dashboard

## 📱 Funcionalidades Disponibles

### Panel de Clientes (`/clients/`)
- ✅ Registro y login
- ✅ Dashboard personalizado
- ✅ Crear proyectos
- ✅ Subir archivos
- ✅ Ver cotizaciones
- ✅ Gestión de perfil

### Panel Administrativo (`/administrador/`)
- ✅ Dashboard de administración
- ✅ Ver todos los proyectos
- ✅ Filtrar por estado/prioridad
- ✅ Actualizar estado de proyectos
- ✅ Enviar cotizaciones
- ✅ Gestionar clientes
- ✅ Ver estadísticas

### Sitio Público
- ✅ Landing page
- ✅ Portafolio
- ✅ Servicios
- ✅ Testimonios
- ✅ Formulario de contacto

## 💡 Tips

1. **Free Tier de Render:**
   - El servicio se duerme después de 15 min de inactividad
   - Primera carga puede tardar 30-50 segundos
   - Para mantenerlo activo, considera plan pagado o usa UptimeRobot

2. **Archivos Media:**
   - Los archivos subidos se pierden en Free tier al reiniciar
   - Para producción, configura AWS S3 o similar

3. **Performance:**
   - Free tier: 512 MB RAM, compartido CPU
   - Para producción seria, considera Starter ($7/mes)

## 📞 Soporte

- **Render Docs:** https://render.com/docs
- **Django Docs:** https://docs.djangoproject.com/
- **GitHub Issues:** Crea issues en tu repo

## ✅ Checklist Final

Antes de considerar el deployment completo:

- [ ] Todas las variables de entorno configuradas
- [ ] Database conectada y migrations aplicadas
- [ ] Superusuario creado
- [ ] Datos iniciales poblados
- [ ] Archivos estáticos funcionando
- [ ] Login de clientes funciona
- [ ] Login de admin funciona
- [ ] Crear proyecto funciona
- [ ] Subir archivos funciona
- [ ] Email configurado (opcional)
- [ ] DNS configurado (si usas dominio propio)

---

**¡Tu aplicación Aplyfly está lista para producción! 🎉**
