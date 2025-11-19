#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const LOGO_PATH = path.join(__dirname, 'logo', 'icono.PNG');
const PUBLIC_PATH = path.join(__dirname, 'public');

async function generateFaviconIco() {
  try {
    console.log('🎨 Generando favicon.ico desde logo/icono.PNG...');
    
    const logoBuffer = fs.readFileSync(LOGO_PATH);
    
    // Generar ICO desde el logo (convertir a PNG primero)
    const pngBuffer = await sharp(logoBuffer)
      .resize(32, 32, {
        fit: 'contain',
        background: { r: 15, g: 23, b: 42, alpha: 1 } // #0f172a
      })
      .png()
      .toBuffer();

    // Crear ICO simple copiando el PNG como ICO
    // En navegadores modernos, esto funciona igual
    const icoPath = path.join(PUBLIC_PATH, 'favicon.ico');
    fs.writeFileSync(icoPath, pngBuffer);
    
    console.log('✅ favicon.ico generado correctamente (32x32)');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

generateFaviconIco();
