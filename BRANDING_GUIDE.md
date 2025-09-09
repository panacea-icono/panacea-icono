# 🎨 Guía de Branding - Panacea Icono S.A.

## 🏥 Identidad Corporativa

### Logo Principal
- **Archivo**: `public/assets/logo-panacea.svg`
- **Uso**: Logo circular para favicon y elementos pequeños
- **Dimensiones**: 200x200px (escalable)

### Logo Médico
- **Archivo**: `public/assets/logo-medical.svg`
- **Uso**: Logo horizontal para documentación y headers
- **Dimensiones**: 300x150px (escalable)

### Favicon
- **Archivo**: `public/assets/icon-favicon.svg`
- **Uso**: Icono de pestaña del navegador
- **Dimensiones**: 32x32px

## 🎨 Paleta de Colores

### Colores Principales
- **Azul Médico Profundo**: `#1a365d` - Color principal de la marca
- **Azul Médico Medio**: `#2d5a87` - Color secundario
- **Rojo de Emergencia**: `#e53e3e` - Color de acento y alertas
- **Verde de Éxito**: `#38a169` - Confirmaciones y estados positivos
- **Amarillo de Advertencia**: `#d69e2e` - Alertas y precauciones
- **Azul Informativo**: `#3182ce` - Información y enlaces

### Colores de Texto
- **Texto Principal**: `#2d3748` - Títulos y texto importante
- **Texto Secundario**: `#718096` - Subtítulos y texto descriptivo
- **Texto Claro**: `#a0aec0` - Texto de apoyo
- **Texto Blanco**: `#ffffff` - Texto sobre fondos oscuros

### Colores de Fondo
- **Fondo Principal**: `#f7fafc` - Fondo general
- **Fondo Secundario**: `#ffffff` - Fondos de tarjetas y contenido
- **Fondo Oscuro**: `#1a202c` - Fondos de headers y elementos destacados
- **Gradiente**: `linear-gradient(135deg, #f7fafc 0%, #e6fffa 100%)`

## 📐 Espaciado y Radios

### Espaciado
- **XS**: `0.25rem` (4px)
- **SM**: `0.5rem` (8px)
- **MD**: `1rem` (16px)
- **LG**: `1.5rem` (24px)
- **XL**: `2rem` (32px)
- **2XL**: `3rem` (48px)

### Radios de Borde
- **SM**: `4px` - Elementos pequeños
- **MD**: `8px` - Elementos estándar
- **LG**: `12px` - Tarjetas y contenedores
- **XL**: `16px` - Elementos grandes

## 🔤 Tipografía

### Fuentes Principales
- **Sistema**: `'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`
- **Monospace**: `'Fira Code', 'Consolas', 'Monaco', monospace`

### Tamaños
- **H1**: `3em` (48px) - Títulos principales
- **H2**: `2em` (32px) - Títulos de sección
- **H3**: `1.4em` (22px) - Subtítulos
- **Body**: `1rem` (16px) - Texto principal
- **Small**: `0.875rem` (14px) - Texto secundario

## 🖼️ Uso de Imágenes

### Logos en Documentación
```markdown
<div align="center">
  <img src="public/assets/logo-medical.svg" alt="Panacea Icono S.A. Logo" width="300" height="150">
</div>
```

### Logos en HTML
```html
<img src="assets/logo-panacea.svg" alt="Panacea Icono S.A. Logo" class="main-logo">
```

### Favicon
```html
<link rel="icon" type="image/svg+xml" href="assets/icon-favicon.svg">
```

## 🎯 Aplicación del Branding

### Archivos Actualizados
- ✅ `public/index.html` - Landing ejecutiva
- ✅ `main_integrated.py` - Dashboard de API
- ✅ `README.md` - Documentación principal
- ✅ `docs/README.md` - Documentación técnica
- ✅ `public/assets/brand-colors.css` - Variables CSS

### Elementos de Branding
- ✅ Logos corporativos en SVG
- ✅ Paleta de colores médicos
- ✅ Tipografía consistente
- ✅ Espaciado uniforme
- ✅ Iconografía médica
- ✅ Gradientes corporativos

## 🔄 Sincronización

### Colores CSS
Todos los colores están definidos en `public/assets/brand-colors.css` y se pueden usar con:
```css
color: var(--panacea-primary);
background: var(--panacea-bg-gradient);
border: 1px solid var(--panacea-border);
```

### Clases Utilitarias
```css
.text-panacea-primary { color: var(--panacea-primary); }
.bg-panacea-accent { background-color: var(--panacea-accent); }
.border-panacea-success { border-color: var(--panacea-success); }
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Adaptaciones
- Logos escalables con SVG
- Colores consistentes en todos los dispositivos
- Tipografía legible en todas las resoluciones
- Espaciado proporcional

## 🏥 Identidad Médica

### Elementos Visuales
- Cruz médica en logos
- Colores que transmiten confianza y profesionalismo
- Iconografía relacionada con medicina y tecnología
- Diseño limpio y profesional

### Mensaje Corporativo
- Medicina Estética y Cirugía Plástica
- Tecnología de vanguardia (IA, Web3, Blockchain)
- Ubicación: Santa Cruz de la Sierra, Bolivia
- Contacto profesional y accesible

---

*Última actualización: 2025-09-09*
*Versión: v2025.09.09.0302*
