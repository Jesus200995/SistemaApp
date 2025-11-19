#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SVG_PATH = path.join(__dirname, 'public', 'favicon.svg');
const PUBLIC_PATH = path.join(__dirname, 'public');

async function generateFaviconIco() {
  try {
    const svgBuffer = fs.readFileSync(SVG_PATH);
    
    // Generar ICO desde el SVG (convertir a PNG primero)
    const pngBuffer = await sharp(svgBuffer)
      .resize(32, 32, {
        fit: 'contain',
        background: { r: 0, g: 0, b: 0, alpha: 0 }
      })
      .png()
      .toBuffer();

    // Crear ICO simple copiando el PNG como ICO
    // En navegadores modernos, esto funciona igual
    const icoPath = path.join(PUBLIC_PATH, 'favicon.ico');
    fs.writeFileSync(icoPath, pngBuffer);
    
    console.log('✓ favicon.ico generado correctamente (32x32)');
    
  } catch (error) {
    console.error('Error generando favicon.ico:', error.message);
  }
}

generateFaviconIco();
