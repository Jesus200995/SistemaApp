#!/usr/bin/env node

/**
 * Script para generar ícono PWA
 * 
 * Uso:
 * node generate-icons.js
 * 
 * O con npm:
 * npm install sharp
 * node generate-icons.js
 * 
 * Este script crea los ícono necesarios desde un SVG o PNG base
 */

const fs = require('fs');
const path = require('path');

// Color del ícono (verde como el tema de la app)
const COLORS = {
  primary: '#10b981',    // Verde principal
  secondary: '#059669',  // Verde oscuro
};

console.log('📱 Generador de Ícono PWA\n');

// Mensaje de instrucciones si no tienes sharp instalado
console.log('Para generar ícono PWA, sigue estos pasos:\n');

console.log('1. Opción A - Usando Figma Online (Recomendado):\n');
console.log('   - Abre: https://www.figma.com');
console.log('   - Crea un cuadrado 512x512');
console.log('   - Color fondo: #10b981 (verde principal)');
console.log('   - Agrega tu logo/texto "🌱 SistemaApp"');
console.log('   - Exporta como PNG 512x512');
console.log('   - Guarda como: public/pwa-512x512.png\n');

console.log('2. Opción B - Usando ImageMagick (Terminal):\n');
console.log('   # Crear imagen base (fondo verde con ícono)');
console.log('   convert -size 512x512 xc:#10b981 public/pwa-512x512.png\n');
console.log('   # Crear 192x192');
console.log('   convert public/pwa-512x512.png -resize 192x192 public/pwa-192x192.png\n');
console.log('   # Crear Apple touch icon');
console.log('   convert public/pwa-512x512.png -resize 180x180 public/apple-touch-icon.png\n');

console.log('3. Opción C - Usar editor online:\n');
console.log('   - Abre: https://www.pixlr.com/online-photo-editor');
console.log('   - Crear imagen 512x512');
console.log('   - Color: #10b981');
console.log('   - Agregar logo/texto');
console.log('   - Exportar como PNG\n');

console.log('4. Opción D - Usar ícono SVG:\n');
console.log('   - Crea SVG en: public/logo.svg');
console.log('   - Usa convertidor online: https://convertio.co/es/svg-png/');
console.log('   - Exportar en 512x512 y 192x192\n');

console.log('5. Opción E - Instalar sharp y ejecutar script:\n');
console.log('   npm install sharp');
console.log('   node generate-icons.js\n');

console.log('✅ Una vez tengas los ícono en public/:\n');
console.log('   - pwa-512x512.png');
console.log('   - pwa-192x192.png');
console.log('   - apple-touch-icon.png (180x180)\n');

console.log('💡 Ícono Maskable (opcional):\n');
console.log('   Los mismos ícono funcionan como "maskable"');
console.log('   Se usan pwa-*-maskable.png pero pueden ser iguales\n');

console.log('🎨 Recomendaciones de Diseño:\n');
console.log('   - Fondo sólido: #10b981 (verde)');
console.log('   - Ícono centrado');
console.log('   - Margen seguro: 10-15% desde bordes');
console.log('   - Color texto: Blanco (#ffffff)');
console.log('   - Sin transparencias (PWA needs opaque)\n');

console.log('📁 Ubicación final:\n');
console.log('   Frontend/sistemaapp-frontend/public/');
console.log('   ├── pwa-512x512.png');
console.log('   ├── pwa-192x192.png');
console.log('   ├── pwa-512x512-maskable.png (igual o similar)');
console.log('   ├── pwa-192x192-maskable.png (igual o similar)');
console.log('   └── apple-touch-icon.png\n');

// Intentar usar sharp si está disponible
try {
  const sharp = require('sharp');
  
  console.log('\n✅ sharp detectado, generando ícono...\n');
  
  // Crear ícono SVG base
  const svgBase = `
    <svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
      <rect width="512" height="512" fill="${COLORS.primary}"/>
      <circle cx="256" cy="256" r="180" fill="${COLORS.secondary}"/>
      <text x="256" y="280" font-size="80" fill="white" text-anchor="middle" font-weight="bold">🌱</text>
      <text x="256" y="360" font-size="40" fill="white" text-anchor="middle" font-weight="bold">SistemaApp</text>
    </svg>
  `;
  
  const publicDir = path.join(__dirname, 'public');
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }
  
  // Guardar SVG
  const svgPath = path.join(publicDir, 'logo.svg');
  fs.writeFileSync(svgPath, svgBase);
  
  console.log('✅ SVG base creado: public/logo.svg');
  
  // Generar 512x512
  sharp(Buffer.from(svgBase))
    .png()
    .toFile(path.join(publicDir, 'pwa-512x512.png'), (err, info) => {
      if (err) console.error('Error generando 512x512:', err);
      else console.log('✅ Generado: public/pwa-512x512.png');
      
      // Generar 192x192
      sharp(path.join(publicDir, 'pwa-512x512.png'))
        .resize(192, 192)
        .toFile(path.join(publicDir, 'pwa-192x192.png'), (err) => {
          if (err) console.error('Error generando 192x192:', err);
          else console.log('✅ Generado: public/pwa-192x192.png');
          
          // Generar apple-touch-icon
          sharp(path.join(publicDir, 'pwa-512x512.png'))
            .resize(180, 180)
            .toFile(path.join(publicDir, 'apple-touch-icon.png'), (err) => {
              if (err) console.error('Error generando apple-touch-icon:', err);
              else console.log('✅ Generado: public/apple-touch-icon.png');
              
              // Copiar como maskable
              fs.copyFileSync(
                path.join(publicDir, 'pwa-512x512.png'),
                path.join(publicDir, 'pwa-512x512-maskable.png')
              );
              console.log('✅ Generado: public/pwa-512x512-maskable.png');
              
              fs.copyFileSync(
                path.join(publicDir, 'pwa-192x192.png'),
                path.join(publicDir, 'pwa-192x192-maskable.png')
              );
              console.log('✅ Generado: public/pwa-192x192-maskable.png');
              
              console.log('\n✨ ¡Ícono PWA generado exitosamente!');
              console.log('Los ícono están en: public/');
            });
        });
    });
    
} catch (err) {
  console.log('ℹ️ sharp no instalado (opcional)\n');
}
