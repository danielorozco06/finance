# FAQ

## Que es una orden limite y una orden de mercado?

Hay dos tipos principales de órdenes:

1. Orden Límite:
   - Especificas el precio exacto al que quieres comprar/vender
   - Solo se ejecuta a ese precio o mejor
   - Ejemplo para CELSIA:
     - Orden límite de compra a 3,500 COP
     - Solo comprará si el precio baja a 3,500 o menos
     - No se ejecutará si el precio se mantiene por encima
   - Ventajas:
     - Control exacto del precio
     - Mejor para planificar entradas/salidas
     - Evita sorpresas en el precio
   - Desventajas:
     - Puede no ejecutarse nunca
     - Puedes perder oportunidades si el precio no llega
2. Orden de Mercado:
   - Compra/vende inmediatamente al mejor precio disponible
   - Se ejecuta al precio que haya en ese momento
   - Ejemplo:
     - Si CELSIA cotiza a 3,630 COP
     - Una orden de mercado comprará inmediatamente
     - Pero podría ejecutarse a 3,635 o más
   - Ventajas:
     - Ejecución inmediata garantizada
     - Útil en situaciones urgentes
   - Desventajas:
     - No controlas el precio exacto
     - Puede haber deslizamiento (ejecutarse a peor precio)

Por eso en el portafolio:

- Usamos órdenes límite para entradas planificadas y take profits
- Reservamos órdenes de mercado para situaciones de emergencia (stops)

## Cuando usar ordenes limite y ordenes de mercado?

Las órdenes límite y de mercado se usan en diferentes situaciones:
Órdenes Límite:

1. Para Entradas:
   - Cuando queremos asegurar un precio específico de compra
   - En niveles técnicos importantes (soportes)
   - Para entradas escalonadas planificadas
   - En acciones con poca liquidez
2. Para Salidas (Take Profit):
   - Para asegurar precio de venta en objetivos
   - En niveles de resistencia técnica
   - Cuando no hay urgencia de salir

Órdenes de Mercado:

1. Para Entradas:
   - Cuando hay una ruptura alcista importante
   - Si necesitamos entrada inmediata por catalizador
   - En acciones muy líquidas
2. Para Salidas:
   - Cuando se activa un stop loss
   - En situaciones de emergencia
   - Cuando hay noticias negativas inesperadas
   - Si el precio está cayendo rápidamente

Por eso en el portafolio:

- Usamos órdenes límite para entradas planificadas
- Pero podríamos usar órdenes de mercado para stops loss en caídas rápidas

## Que es el timing?

El "timing" se refiere a la distribución temporal de las compras - cuándo y en qué proporción se ejecutarán las órdenes de entrada.

Por ejemplo, para CELSIA:

- Timing: "60% inmediato, 40% en pullback" significa:

1. Comprar 60% de la posición ahora (COP 1,800,000)
2. Esperar a que el precio baje para comprar el 40% restante (COP 1,200,000)

Para cada acción tenemos un timing diferente:

1. CELSIA
   - 60% inmediato = COP 1,800,000 a 3,630 COP
   - 40% en pullback = COP 1,200,000 a 3,500 COP

## Que quiere decir TP1 y TP2?

TP1 y TP2 significan "Take Profit 1" y "Take Profit 2" - son los objetivos de precio para tomar ganancias.
Por ejemplo, para CELSIA:

1. TP1 (Take Profit 1): 3,800 COP
   - Es el primer objetivo de precio
   - Cuando se alcanza, vendemos el 60% de la posición
   - Representa una ganancia de +4.7% desde el precio de entrada
2. TP2 (Take Profit 2): 4,000 COP
   - Es el segundo objetivo de precio
   - Para el 40% restante de la posición
   - Representa una ganancia de +10.2% desde el precio de entrada

La estrategia escalonada de toma de ganancias (60%/40%) permite:

1. Asegurar ganancias en TP1 con la mayor parte de la posición
2. Mantener exposición para mayor potencial con TP2
3. Reducir el riesgo después de alcanzar TP1

## Que es pullback?

Un pullback es un retroceso temporal en el precio de una acción después de un movimiento alcista. Es una oportunidad para entrar a un mejor precio.
Por ejemplo, en CELSIA:

- Precio actual: 3,630 COP
- Pullback esperado: hacia 3,500 COP (soporte)

La estrategia de entrada escalonada aprovecha los pullbacks:

1. Primera orden (60%): 3,630 COP - entrada inmediata
2. Segunda orden (40%): 3,500 COP - esperar pullback al soporte

Beneficios de esperar pullbacks:

1. Mejor precio promedio de entrada
2. Entrada en niveles de soporte técnico
3. Mejor relación riesgo/retorno

Por eso el plan tiene "timing" diferente para cada acción:

- CELSIA: 60% inmediato, 40% en pullback
- CONCONCRET: 70% inmediato, 30% en pullback
- MINEROS: 100% inmediato (no esperar pullback)
- PFGRUPSURA: 60% inmediato, 40% en pullback
- ISA: 50% inmediato, 50% en pullback

## Que quiere decir Mantener órdenes límite activas por máximo 2 días?

Esta regla significa que si una orden límite no se ejecuta dentro de 2 días, se debe reevaluar el precio y la estrategia. La razón es:

1. Si una orden límite no se ejecuta en 2 días, probablemente significa que:
   - El mercado se está moviendo en contra de nuestra expectativa
   - El precio objetivo ya no es relevante
   - Las condiciones del mercado han cambiado
2. Qué hacer después de los 2 días:
   - Revisar el análisis técnico actualizado
   - Evaluar si el nivel de entrada sigue siendo válido
   - Decidir si:
     - Ajustar el precio límite
     - Esperar un mejor punto de entrada
     - Cancelar la orden y reevaluar la estrategia
3. Por ejemplo, para CELSIA:
   - Si la orden límite a 3,630 COP no se ejecuta en 2 días
   - Y el precio sigue subiendo
   - Debemos decidir si:
     - Subir el precio límite para no perder la tendencia
     - O esperar un retroceso al siguiente soporte

## Que es un stop loss?

Un stop loss es una orden de venta automática que se activa cuando el precio cae hasta cierto nivel, diseñada para limitar pérdidas.
Por ejemplo, en CELSIA:

1. Precio de entrada: 3,630 COP
2. Stop Loss: 3,400 COP
3. Si el precio cae a 3,400 COP:
   - Se activa la orden de venta automática
   - Limita la pérdida a -6.3% (COP 189,000)
   - Protege el capital de mayores caídas

Tipos de Stop Loss:

1. Stop Loss Normal:
   - Se convierte en orden de mercado al tocar el precio
   - Ejecución inmediata pero puede tener deslizamiento
2. Stop Límite:
   - Se convierte en orden límite al tocar el precio
   - Asegura precio pero puede no ejecutarse

En el portafolio usamos stops por:

1. Protección individual:
   - CELSIA: 3,400 COP (-6.3%)
   - CONCONCRET: 380 COP (-11.4%)
   - MINEROS: 4,000 COP (-8.0%)
   - PFGRUPSURA: 25,000 COP (-4.0%)
   - ISA: 15,500 COP (-5.7%)
2. Protección global:
   - Stop loss del portafolio: -8% (COP 960,000)
   - Se sale de todas las posiciones si la pérdida total llega a este nivel

## Que quiere decir activacion en ordenes de proteccion?

"Activación" en órdenes de protección (stop loss) se refiere a cuándo colocar la orden de stop loss. Veamos los diferentes casos del portafolio:

1. "Activación: Después de llenar órdenes de entrada" (CELSIA)
   - Esperar a que se ejecuten ambas órdenes de compra
   - Solo entonces colocar el stop loss a 3,400 COP
   - Porque tendremos un precio promedio de entrada
2. "Activación: Inmediata después de cada compra" (CONCONCRET)
   - Colocar un stop loss por cada orden que se ejecute
   - Primera compra → primer stop loss
   - Segunda compra → segundo stop loss
   - Protección inmediata por alta volatilidad

## Que es breakeven?

Breakeven (o punto de equilibrio) es el precio de entrada original donde no hay ni ganancia ni pérdida.
La regla "Al alcanzar TP1, ajustar stop loss a breakeven" significa que:

1. Cuando el precio alcance el primer objetivo (TP1) y vendamos el 60% de la posición:
   - Movemos el stop loss al precio de entrada
   - Así aseguramos que en el 40% restante de la posición no podemos perder dinero
2. Por ejemplo, para CELSIA:
   - Entrada: 3,630 COP
   - TP1: 3,800 COP (vendemos 60%)
   - Stop loss inicial: 3,400 COP
   - Después de alcanzar TP1, movemos el stop loss a 3,630 COP (breakeven)
   - Así el 40% restante de la posición ya no puede dar pérdidas

## Que quiere decir Evaluar trailing stop después de alcanzar TP1?

El trailing stop es un stop loss móvil que "sigue" al precio mientras sube, manteniendo una distancia fija o porcentual.
"Evaluar trailing stop después de alcanzar TP1" significa que:

1. Después de alcanzar el primer objetivo (TP1):
   - En lugar de dejar un stop loss fijo en breakeven
   - Podemos usar un stop loss que se mueva con el precio
   - Para proteger las ganancias pero dar espacio al precio para llegar a TP2
2. Por ejemplo, para CELSIA:
   - Entrada: 3,630 COP
   - TP1: 3,800 COP (vendemos 60%)
   - TP2: 4,000 COP (objetivo para el 40% restante)
   - Podríamos usar un trailing stop de 200 puntos:
     - Si el precio sube a 3,850 → stop sube a 3,650
     - Si sube a 3,900 → stop sube a 3,700
     - Si sube a 3,950 → stop sube a 3,750
   - Así protegemos ganancias pero damos espacio para alcanzar TP2
