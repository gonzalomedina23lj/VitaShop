# VitaShop — tienda independiente

Versión de revisión del catálogo público de https://vitashop.com.ar, recuperado el 12 de octubre de 2026. Código propio sin dependencias de Tiendanube ni de Mercado Libre para la interfaz. No procesa pagos ni genera pedidos.

Se recuperaron 332 productos, 327 fotografías principales y 4 fotografías adicionales. Cinco imágenes principales pendientes aparecen identificadas con una ilustración de reemplazo; los productos están detallados en `migration-report.json`. Las galerías originales reúnen 935 URLs; las fotografías adicionales todavía requieren completar la exportación. La vista muestra únicamente imágenes locales.

## Ejecutar

Servir `dist/` con un servidor HTTP. No abrir `index.html` directamente mediante `file://`, porque el catálogo se carga con `fetch`.

```sh
python3 -m http.server 8000 --directory dist
```

Pruebas: `node --test test-store.cjs`.

## Funciones implementadas

- Catálogo público, imágenes principales locales y fichas de producto.
- Búsqueda por nombre, marca, ingrediente y presentación.
- Filtros por categoría, marca, ingrediente, disponibilidad, precio y descuento.
- Orden por precio o nombre, paginación y enlaces individuales de producto.
- Carrito local persistente con cantidades, eliminación y cálculo de subtotal.
- Recorrido de revisión con selección visual de medio de pago y consulta de código postal, sin tarifas ficticias, sin cobros y sin registro de pedidos.
- Adaptación a celulares, etiquetas accesibles, navegación con teclado y diálogos nativos.

## Alcance de la migración

`dist/assets/catalogue.json` contiene los datos públicos recuperados y sus URLs de origen. El precio y la disponibilidad son una fotografía del sitio al momento de la extracción, no un inventario sincronizado. Las categorías de navegación son una reorganización propia; se conservan las categorías originales recuperadas de las fichas. No se incorporaron recomendaciones médicas ni beneficios adicionales.

No se ha migrado la base de datos privada: stock exacto por unidad y variante, SKU internos no publicados, pedidos, clientes, accesos, configuración de cobro y contratos logísticos. Para completar esos datos se necesita una exportación autorizada del administrador de Tiendanube. Antes de cerrar la tienda actual, obtener también las imágenes originales en su máxima resolución.

Las URLs de las galerías originales se conservan como metadatos. Solo las imágenes descargadas y verificadas se muestran en la nueva galería. La réplica no depende del CDN de Tiendanube para las fotos que muestra.

## Activar ventas

Esta versión es una interfaz estática. Para una tienda operativa agregar un servidor con base de datos y administración autenticada. Validar precios, disponibilidad y variantes en el servidor; el carrito local nunca debe ser una fuente confiable para un cobro.

1. Importar y conciliar catálogo, SKU, variantes, cantidades, pesos y dimensiones desde la exportación del comercio.
2. Incorporar una base de datos de productos, pedidos, pagos y movimientos de inventario; panel de administración con acceso privado.
3. Mercado Pago: usar credenciales del comercio solo en el servidor, crear preferencias con precios obtenidos de la base de datos y confirmar pagos mediante notificaciones verificadas e idempotentes. No marcar un pedido como pagado por una URL de retorno.
4. Transferencia: configurar titular, CBU/alias y condiciones aprobadas. Pedidos en estado pendiente; comprobante revisado antes de marcar pagado.
5. Envíos: tarifas por zonas/código postal o integración con transportista mediante cuenta del comercio. Cotizar con peso, dimensiones y origen reales, definir plazos, etiquetas y seguimiento. No asumir que una tarifa de la tienda actual corresponde a cualquier domicilio.
6. Configurar condiciones de compra, cambios, privacidad y atención del comercio; probar pagos de prueba, disponibilidad concurrente, cancelaciones y conciliación.
7. Apuntar el dominio propio al alojamiento definitivo después de validar la tienda.

## GitHub y alojamiento

El código puede guardarse en un repositorio de GitHub. GitHub Pages restringe el alojamiento de tiendas cuya finalidad principal es facilitar transacciones comerciales y no proporciona un servidor para el checkout. Usar un alojamiento apto para comercio electrónico con servidor o funciones y base de datos. No se configuró un workflow para desplegar ventas en GitHub Pages.

Referencias oficiales:
- https://docs.github.com/es/pages/getting-started-with-github-pages/github-pages-limits
- https://www.mercadopago.com.ar/developers/es/docs/checkout-pro-preferences/overview
- https://ayuda.tiendanube.com/es_AR/como-descargar-la-lista-de-productos-de-mi-tiendanube

## Estructura

- `dist/index.html`, `style.css`, `app.js`, `store-core.js`: sitio estático.
- `dist/assets/catalogue.json`: catálogo normalizado y procedencia.
- `dist/assets/products/`: fotografías locales.
- `dist/productos/<slug>/index.html`: enlaces de producto independientes.
- `scripts/prepare-catalogue.py`: normalización, inventario de imágenes y generación de páginas.
- `test-store.cjs`: pruebas de búsqueda, descuentos, carrito y subtotal.
- `.openai/hosting.json`: configuración del alojamiento de la vista privada.

## Verificación

Se verifican sintaxis JavaScript, cálculos, filtros, recuperación del carrito, integridad del catálogo y presencia de fotografías. La revisión visual mediante navegador de la nueva vista no se ejecuta cuando el entorno no ofrece la herramienta de control de navegador requerida por Sites.
