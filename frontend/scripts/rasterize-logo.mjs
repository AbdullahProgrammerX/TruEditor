/**
 * Rasterize public/logo-icon.svg → PNGs (favicon, apple-touch, OG).
 * Run: node scripts/rasterize-logo.mjs
 */
import sharp from 'sharp'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const pub = join(__dirname, '..', 'public')
const svgPath = join(pub, 'logo-icon.svg')
const svg = readFileSync(svgPath)

const pad = { fit: 'contain' }

await sharp(svg)
  .resize(512, 512, { ...pad, background: { r: 0, g: 0, b: 0, alpha: 0 } })
  .png()
  .toFile(join(pub, 'logo-icon.png'))

await sharp(svg)
  .resize(192, 192, { ...pad, background: { r: 247, g: 249, b: 250, alpha: 1 } })
  .png()
  .toFile(join(pub, 'favicon.png'))

await sharp(svg)
  .resize(180, 180, { ...pad, background: { r: 247, g: 249, b: 250, alpha: 1 } })
  .png()
  .toFile(join(pub, 'apple-touch-icon.png'))

const logoBuf = await sharp(svg)
  .resize(300, 300, { ...pad, background: { r: 0, g: 0, b: 0, alpha: 0 } })
  .png()
  .toBuffer()

const left = 1200 - 300 - 64
const top = Math.round((630 - 300) / 2)

await sharp({
  create: {
    width: 1200,
    height: 630,
    channels: 3,
    background: { r: 30, g: 58, b: 95 },
  },
})
  .composite([{ input: logoBuf, left, top }])
  .png()
  .toFile(join(pub, 'og-image.png'))

console.log('Rasterized logo-icon.svg → logo-icon.png, favicon.png, apple-touch-icon.png, og-image.png')
