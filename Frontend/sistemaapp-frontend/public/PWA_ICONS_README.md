# 📱 Íconos PWA

## Cómo generar los íconos PWA

Los íconos PWA se deben crear con las siguientes dimensiones:

### Iconos requeridos:

1. **pwa-192x192.png** (192x192 píxeles)
2. **pwa-512x512.png** (512x512 píxeles)
3. **apple-touch-icon.png** (180x180 píxeles - para iOS)

## Generación automática

### Opción 1: Usar favicon.io
1. Ve a https://favicon.io
2. Sube tu imagen/logo
3. Descarga todos los formatos
4. Selecciona los archivos PNG necesarios
5. Copia a la carpeta `public/`

### Opción 2: Usar PWA Builder
1. Ve a https://www.pwabuilder.com/
2. Carga tu imagen
3. Genera los íconos automáticamente
4. Descarga el paquete

### Opción 3: Usar Canva
1. Crea un diseño en https://www.canva.com
2. Exporta en PNG
3. Usa ImageMagick o similar para redimensionar:

```bash
# Instalar ImageMagick si no lo tienes
# macOS: brew install imagemagick
# Windows: descarga desde imagemagick.org
# Linux: sudo apt install imagemagick

# Redimensionar imagen
convert logo.png -resize 192x192 pwa-192x192.png
convert logo.png -resize 512x512 pwa-512x512.png
convert logo.png -resize 180x180 apple-touch-icon.png
```

## Colores recomendados para SistemaApp

- **Color primario**: #16a34a (Verde)
- **Fondo**: #ffffff (Blanco)
- **Tema**: Profesional, ambiental, territorial

## Especificaciones técnicas

| Archivo | Dimensión | Formato | Ubicación |
|---------|-----------|---------|-----------|
| pwa-192x192.png | 192x192 | PNG | public/ |
| pwa-512x512.png | 512x512 | PNG | public/ |
| apple-touch-icon.png | 180x180 | PNG | public/ |
| favicon.ico | 64x64+ | ICO | public/ |

## Después de crear los íconos

1. Copia los archivos a `Frontend/sistemaapp-frontend/public/`
2. Reinicia `npm run dev`
3. La PWA reconocerá automáticamente los íconos

## Para testing

Mientras no tengas los íconos, puedes usar cualquier imagen PNG:

```bash
# Crear un icono provisional (requiere imagemagick)
convert xc:#16a34a -size 192x192 pwa-192x192.png
convert xc:#16a34a -size 512x512 pwa-512x512.png
convert xc:#16a34a -size 180x180 apple-touch-icon.png
```

## Verificar que los íconos se instalan

1. Abre DevTools (F12)
2. Ve a Manifest en Application tab
3. Verifica que los íconos aparezcan en "Icons"
4. Instala la app (botón de instalación en la barra de direcciones)

---

**Nota:** Los íconos son opcionales para el desarrollo, pero recomendados para producción.

