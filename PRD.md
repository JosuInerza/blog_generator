**PRD: Validación SEO de título y descripción + Generación de slug**

**Propósito**:
- Proveer una API que valide un `title` y una `description` para posts orientados a SEO y devuelva un `slug` listo para usar en URLs.

**Alcance**:
- Validación sintáctica y semántica básica orientada a SEO.
- Generación determinista de `slug` a partir del título (con reglas de normalización y truncado).
- Respuesta con errores, advertencias y sugerencias de mejora.

**Stakeholders**:
- Product Owner: responsable de requisitos de SEO.
- Equipo Backend: implementación de la API.
- Equipo Frontend: integración del servicio para previsualizar y guardar posts.
- QA: verificar criterios y pruebas automatizadas.

**Definiciones**:
- `title`: título del post (texto corto, objetivo para buscadores).
- `description`: descripción o meta description del post (resumen corto para SERP).
- `slug`: versión url-safe del `title` (minúsculas, guiones, sin caracteres especiales).
- `SEO score`: métrica discreta (0-100) que resume la calidad SEO según reglas definidas.

**Requisitos de Usuario (ejemplos)**:
- Como autor, quiero validar mi título para que sea óptimo para motores de búsqueda.
- Como editor, necesito una descripción que quepa en resultados de búsqueda y contenga la keyword principal.
- Como desarrollador, quiero recibir un `slug` válido directamente para usar en la URL del post.

**Requisitos Funcionales (RF)**:
- RF1: Endpoint que reciba `title` y `description` y devuelva validación + `slug`.
- RF2: Validar longitud mínima y máxima del `title`.
- RF3: Validar longitud mínima y máxima del `description`.
- RF4: Detectar presencia de la palabra clave principal en `title` y `description` (opcional: si se recibe `keyword`).
- RF5: Identificar palabras repetidas en el `title` y advertir sobre "keyword stuffing".
- RF6: Calcular un `SEO score` basado en reglas (longitud, presencia de keyword, legibilidad).
- RF7: Generar `slug` siguiendo reglas definidas (normalización, ASCII, guiones, longitud máxima).
- RF8: Devolver lista de `errors` (errores que invalidan) y `warnings` (recomendaciones).
- RF9: Soportar respuesta en JSON con ejemplos claros y códigos HTTP apropiados.

**Requisitos No Funcionales (RNF)**:
- RNF1 (Rendimiento): Latencia < 100ms por petición en medianas cargas (p.e. 100 RPS) para el servicio de validación puro.
- RNF2 (Disponibilidad): 99.9% durante horas de publicación.
- RNF3 (Seguridad): Sanitizar entradas para evitar inyección; limitar tamaño máximo de payload (p.e. 10 KB).
- RNF4 (Internacionalización): Soportar títulos en UTF-8; `slug` debe transliterar a ASCII o aplicar punycode si es necesario.
- RNF5 (Escalabilidad): Diseñar para ser stateless (idempotente) y escalable horizontalmente.

**Reglas de Validación (detalladas)**:
- Title:
  - Longitud mínima: 30 caracteres recomendados; longitud absoluta mínima 10.
  - Longitud máxima aconsejada: 60 caracteres (SEO), RPC (absolute) 120.
  - No debe contener sólo stopwords; debe contener al menos una palabra con longitud >= 3.
  - No debe contener múltiples palabras repetidas (>3 repeticiones total) — advertencia de stuffing.
- Description:
  - Longitud mínima recomendada: 70 caracteres; mínima absoluta 30.
  - Longitud máxima aconsejada: 160 caracteres; absoluta 320.
  - Debe ser descriptiva y única (se puede recomendar comprobación de duplicados contra DB si se integra).
- Keyword (opcional):
  - Si se proporciona `keyword`, validar que aparezca en `title` o `description` y dar punto extra en `SEO score`.

**Reglas de generación de `slug`**:
- Normalizar: trim, convertir a minúsculas.
- Translitar caracteres Unicode a ascii cuando sea posible (p.e. `ñ` -> `n`).
- Reemplazar cualquier secuencia de espacios y caracteres no alfanuméricos por un solo guion `-`.
- Eliminar caracteres sobrantes (no permitir `#`, `%`, `?`, etc.).
- Colapsar guiones repetidos `---` -> `-`.
- Quitar guiones al inicio o final.
- Limitar longitud del `slug` a 80 caracteres por defecto; si el título genera slug duplicado en almacenamiento posterior, permitir sufijo `-n` para desambiguar (no gestionado por la API básica a menos que el servicio tenga acceso a almacenamiento).
- Ejemplo: "¡Hola Mundo: guía 2025!" -> `hola-mundo-guia-2025`

**API Spec (Propuesta)**:
- Endpoint: `POST /api/v1/seo/validate`
- Request JSON:
  - `title` (string, requerido)
  - `description` (string, requerido)
  - `keyword` (string, opcional)
  - `max_slug_length` (integer, opcional)
- Response JSON (200):
  - `valid`: boolean (true si no hay `errors` críticos)
  - `errors`: array of {code, message}
  - `warnings`: array of {code, message}
  - `seo_score`: integer (0-100)
  - `slug`: string | null (slug generado si `title` válido)
  - `suggestions`: object (e.g., recommended title, trimmed description)
- Códigos de estado:
  - 200: petición válida, con `errors`/`warnings` según el caso.
  - 400: payload mal formado o falta de campos requeridos.
  - 413: payload demasiado grande.

**Ejemplo de Request**:
{
  "title": "Guía completa de SEO para blogs en 2025",
  "description": "Aprende técnicas prácticas y actualizadas para optimizar tus posts y mejorar el posicionamiento en buscadores.",
  "keyword": "SEO blogs"
}

**Ejemplo de Response**:
{
  "valid": true,
  "errors": [],
  "warnings": [
    {"code": "title_length_long", "message": "El título excede la longitud recomendada (60 chars)."}
  ],
  "seo_score": 87,
  "slug": "guia-completa-de-seo-para-blogs-en-2025",
  "suggestions": {
    "title": "Guía de SEO para blogs (2025)",
    "description": "Optimiza tus posts para buscadores con técnicas prácticas y actualizadas."
  }
}

**Criterios de Aceptación (AC)**:
- AC1: Dado un `title` válido y `description` válidas, el endpoint devuelve `valid: true` y un `slug` que cumple reglas de slug.
- AC2: Dado un `title` demasiado corto (<10) o vacío, el endpoint devuelve 400 o `errors` relevantes y `valid: false`.
- AC3: Dado una `description` demasiado larga (>320) se devuelve warning y `suggestions` con versión truncada.
- AC4: Si se proporciona `keyword`, se reporta su presencia/ausencia en ambos campos.

**Casos de Prueba Sugeridos (automatizables)**:
- Crear tests unitarios para reglas individuales (longitudes, presencia de keyword, transliteración).
- Test de integración del endpoint con combinaciones comunes y límites (mínimo, recomendado, máximo).
- Tests de `slug` para títulos con Unicode, símbolos y espacios múltiples.

**Métricas y Monitoreo**:
- Métrica: porcentaje de validaciones con `valid: true` vs `valid: false`.
- Latencia P95 y P99.
- Conteo de errores críticos por hora.

**Consideraciones de Diseño e Implementación**:
- Implementación recomendada: `FastAPI` + `pydantic` para validación y modelos.
- Para `slug` usar librería probada (p.e. `python-slugify`) o implementar función propia con `unicodedata.normalize` + regex.
- Mantener lógica stateless; si se necesita evitar slugs duplicados, integrar con almacenamiento (DB) y exponer endpoint para resolver colisiones.
- Extensibilidad: exponer opciones para reglas SEO (configurable por cliente) y soportar perfiles diferentes (blog, news, producto).

**Riesgos y Mitigaciones**:
- Riesgo: reglas SEO cambian frecuentemente. Mitigación: parametrizar reglas y mantener conjunto de tests de aceptación.
- Riesgo: transliteración imperfecta de idiomas no latinos. Mitigación: documentar comportamiento y permitir punycode o usar slug nativo cuando sea necesario.

**Milestones Propuestos**:
- M1 (1 día): Spec completo y prototipo del endpoint con reglas básicas.
- M2 (2-3 días): Implementación completa de validaciones y tests unitarios.
- M3 (1 día): Integración de `slug` y tests de integración.
- M4 (1 día): Documentación y ejemplos, preparar despliegue.

**Anexos / Recursos**:
- Enlaces a guías SEO de referencia (Google Search Central) y buenas prácticas de longitud de meta tags.

---

Fin del documento PRD. Puedes pedirme que lo ajuste (más/menos detalle), añadir reglas específicas de SEO de tu equipo, o generar automáticamente los tests y el endpoint en `FastAPI` a partir de este PRD.
