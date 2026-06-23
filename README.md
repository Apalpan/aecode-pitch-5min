# AECODE — Pitch Deck 5 minutos · 20 slides

Pitch deck de inversión autocontenido (un solo `index.html`, sin build ni dependencias).
Versión condensada para presentar en ~5 minutos. Hermano del *deck maestro* (file de
entendimiento avanzado) — este es el **pitch para jurado / inversionista**.

**Live:** https://apalpan.github.io/aecode-pitch-deck/

## Modo guion (notas del orador)

Cada slide incluye su **guion**. Pulsa **`N`** (o el botón ✎) para abrir el panel de guion del orador
abajo; se actualiza solo al cambiar de slide. Ideal para ensayar o leer en una segunda pantalla.

## Controles

- **Navegar**: `←` / `→` o barra espaciadora · rueda del mouse · clic en los bordes · swipe en móvil.
- **Guion**: `N` o ✎ · **Índice**: `O` o ☰ · **Auto-play**: `P` (≈14 s/slide → ~5 min).
- **Tema**: `T` (mix combinado → oscuro → claro) · **Pantalla completa**: `F`.
- **Responsive**: 16:9 en escritorio; reflow real en móvil/vertical.

## Diseño

Design system OFICIAL AECODE: **Manrope**, navy `#0E1121`, violeta `#4A3AC1`, verde `#17B14E`,
azul `#4465EE`. Light + dark combinado. Logos reales + Aecodito. Gráficas: barras, barras apiladas
(revenue mix), TAM/SAM/SOM, donut (ask), timeline (roadmap) y diagramas de flujo.

## Iterar

Todo el contenido (texto + guion) vive en la lista `SLIDES` de `build_pitch.py`
(cada slide: `S(theme, capítulo, layout, contenido, notes)`). Edita y regenera:

```bash
python build_pitch.py
```

## Estructura (20 slides · minimalista para pitch presencial)

Hook · Oportunidad · Por qué ahora · Problema central · Dolor específico · Solución ·
Producto/Video Demo · Innovación tecnológica · Mercado · Modelo B2C2B · Modelo de negocio ·
Tracción · Go To Market · NSM · Diferenciación · Crecimiento Roadmap · Escalabilidad ·
Equipo · Ask · Cierre.

Cada slide queda con titular + un elemento visual; el detalle vive en el **guion** (tecla `N`).
Cada slide está etiquetado con su sección (barra inferior y barra de capítulos superior).
