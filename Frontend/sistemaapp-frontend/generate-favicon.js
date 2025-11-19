#!/usr/bin/env node

/**
 * Script para generar iconos animados del favicon
 * Convierte el SVG a PNG en diferentes tamaños
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SVG_PATH = path.join(__dirname, 'public', 'favicon.svg');
const PUBLIC_PATH = path.join(__dirname, 'public');

// Configuración de iconos a generar
const ICON_SIZES = [
  { size: 16, name: 'favicon' },
  { size: 32, name: 'favicon-32' },
  { size: 64, name: 'favicon-64' },
  { size: 192, name: 'pwa-192x192' },
  { size: 512, name: 'pwa-512x512' }
];

async function generateIcons() {
  try {
    const svgBuffer = fs.readFileSync(SVG_PATH);
    
    console.log('Generando iconos desde SVG...');
    
    for (const icon of ICON_SIZES) {
      const outputPath = path.join(PUBLIC_PATH, `${icon.name}.png`);
      
      await sharp(svgBuffer)
        .resize(icon.size, icon.size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 }
        })
        .png()
        .toFile(outputPath);
      
      console.log(`✓ Generado: ${icon.name}.png (${icon.size}x${icon.size})`);
    }
    
    // Generar variantes maskable para PWA
    for (const icon of [{size: 192, name: 'pwa-192x192'}, {size: 512, name: 'pwa-512x512'}]) {
      const outputPath = path.join(PUBLIC_PATH, `${icon.name}-maskable.png`);
      
      await sharp(svgBuffer)
        .resize(icon.size, icon.size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 }
        })
        .png()
        .toFile(outputPath);
      
      console.log(`✓ Generado: ${icon.name}-maskable.png (${icon.size}x${icon.size})`);
    }
    
    // Generar favicon.ico de 32x32
    const faviconPath = path.join(PUBLIC_PATH, 'favicon.ico');
    await sharp(svgBuffer)
      .resize(32, 32, {
        fit: 'contain',
        background: { r: 0, g: 0, b: 0, alpha: 0 }
      })
      .png()
      .toFile(faviconPath.replace('.ico', '-temp.png'));
    
    // Si tenemos 'ico' disponible, convertir a ICO
    try {
      const icoLib = await import('ico');
      const pngBuffer = fs.readFileSync(faviconPath.replace('.ico', '-temp.png'));
      const icoBuffer = icoLib.encode([pngBuffer]);
      fs.writeFileSync(faviconPath, icoBuffer);
      fs.unlinkSync(faviconPath.replace('.ico', '-temp.png'));
      console.log('✓ Generado: favicon.ico');
    } catch (e) {
      // Si no está disponible, renombrar PNG como favicon
      fs.renameSync(faviconPath.replace('.ico', '-temp.png'), faviconPath.replace('.ico', '.png'));
      console.log('✓ Generado: favicon.png (ico no disponible)');
    }
    
    console.log('\n✅ Todos los iconos se generaron correctamente');
    
  } catch (error) {
    console.error('❌ Error generando iconos:', error.message);
    process.exit(1);
  }
}

// Ejecutar si se llama directamente
generateIcons();
