#!/usr/bin/env node

/**
 * Script para generar iconos del logo.PNG para usar en favicon y PWA
 * Requiere: npm install sharp
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const logoPath = path.join(__dirname, 'logo', 'icono.PNG');
const publicPath = path.join(__dirname, 'public');

// Crear directorio public si no existe
if (!fs.existsSync(publicPath)) {
  fs.mkdirSync(publicPath, { recursive: true });
}

// Verificar que el logo existe
if (!fs.existsSync(logoPath)) {
  console.error('❌ Error: logo/icono.PNG no encontrado');
  process.exit(1);
}

console.log('🎨 Generando iconos desde logo/icono.PNG...');

// Tamaños a generar
const sizes = [
  { size: 16, name: 'favicon.png' },
  { size: 32, name: 'favicon-32.png' },
  { size: 64, name: 'favicon-64.png' },
  { size: 192, name: 'pwa-192x192.png' },
  { size: 512, name: 'pwa-512x512.png' },
  { size: 192, name: 'pwa-192x192-maskable.png', maskable: true },
  { size: 512, name: 'pwa-512x512-maskable.png', maskable: true },
];

// Generar cada tamaño
Promise.all(
  sizes.map(({ size, name, maskable }) => {
    const outputPath = path.join(publicPath, name);
    console.log(`  📦 Generando ${name} (${size}x${size})...`);

    let transform = sharp(logoPath).resize(size, size, {
      fit: 'contain',
      background: { r: 15, g: 23, b: 42, alpha: 1 }, // #0f172a
    });

    if (maskable) {
      // Para iconos maskable, añadir fondo circular
      transform = transform.png({ quality: 90 });
    } else {
      transform = transform.png({ quality: 90 });
    }

    return transform.toFile(outputPath);
  })
)
  .then(() => {
    console.log('✅ ¡Iconos generados exitosamente!');
    console.log('\n📋 Archivos creados:');
    sizes.forEach(({ name }) => {
      console.log(`   ✓ ${name}`);
    });
    console.log('\n💡 Próximos pasos:');
    console.log('   1. Asegurate que index.html tenga los links correctos a los iconos');
    console.log('   2. Verifica que manifest.json apunte a estos archivos');
    console.log('   3. Recarga el navegador con Ctrl+Shift+R para limpiar cache');
  })
  .catch((err) => {
    console.error('❌ Error generando iconos:', err);
    process.exit(1);
  });
