# Canon Event 3 — Arquitectura para módulos

Mod para **Minecraft 1.20.1 (Forge, loader `lowcodefml`)**: es un datapack + resource pack dentro de un .jar.
**No hay código Java.** Todo es `.mcfunction`, JSON, modelos y texturas.

```
canon-event/
  base/                 mod 2.0.0 original (NO SE TOCA; es la base de cada build)
  tools/
    build.py            base/ -> build/out/ + módulos -> verificación -> .jar
    check.py            verificador (mecha + registros 1.20.1 + referencias)
    preview.py          vista frontal de modelos: preview.py out.png modelo+cabeza ...
    canon/ctx.py        API para módulos (Ctx) + helpers de texto/rigs/ítems
    canon/shim.py       atajos F(), A(), pick(), models()
    canon/models.py     librería de modelos/texturas (Atlas, Part, humanoid_parts, pose, head_parts...)
    canon/registry_1_20_1.json  bloques/ítems/entidades/efectos/partículas/sonidos/biomas válidos
    features/<modulo>.py         UN archivo por módulo (+ opcional features/<modulo>_*.py)
    assets/<modulo>/...          binarios que el módulo copia al build (ogg, png) si los necesita
  docs/ARQUITECTURA.md, docs/LORE.md
```

## Reglas de oro

1. **Solo 1.20.1.** No existen: `/return`, `/random`, `/tick`, macros (`$`), `function ... with`,
   `execute if function`, `scoreboard players display`, componentes de ítems (1.20.5).
   Los ítems usan NBT: `{CustomModelData:N,canon:{id:"x"},display:{Name:'...',Lore:[...]}}`.
   Para azar usa predicados `canon:azar/1enN` (N = 2..12, 20, 40, 60, 100, 150, 200, 250, 300, 400, 600, 1200, 1500, 2400, 6000) o `canon:azar/50`, o `c.pick()`.
2. **Cada módulo escribe solo en sus carpetas** (tabla abajo). Para engancharte al mod usa los ganchos de `Ctx`, nunca edites `extra/*`, `npc2/*`, `rig/frames/extra` a mano.
3. **No llames funciones de otros módulos** (pueden no existir en tu rama). Coordina por *tags* y *marcadores de score* (ver "Convenciones compartidas"). Sí puedes llamar funciones del **mod base** (están en `base/data/canon/functions`).
4. **Textos para jugadores en español**, sin comillas `'` `"` ni `\` (rompen el JSON dentro de NBT). `txt()` lo valida.
5. **`python3 tools/build.py` debe terminar con `0 problemas`** antes de hacer commit. `--only tu_modulo` compila solo core + tu módulo (más rápido). La verificación usa `mecha` (sintaxis oficial) y los registros 1.20.1.
6. Objetivos de scoreboard: `dv.` + máximo 13 caracteres (16 en total). Decláralos con `c.objective()`.
   Constantes `#N dv.math`: decláralas con `c.const(N)` (aunque ya existan en base).
7. Jugadores multijugador: Santi (`tantanto4`, tag `dv_santi` puesto por base `juli/player`), Bana (usuario `Bana` o `bana`), Juan (amigo, usuario desconocido). Todo debe funcionar con 2+ jugadores.

## Cómo es un módulo

```python
# tools/features/mimodulo.py
from canon.shim import *        # F, A, pick, jt, chat, say, bubble, menu, btn, rig_summon, set_cmd, head, item_nbt, loot_item, CMD
from canon import shim
from canon import models as M   # si haces modelos

def build(c):                   # c = canon.ctx.Ctx
    shim.use(c)
    shim.models(['mi_npc_idle', 'mi_npc_walk_a', 'mi_npc_walk_b'], 7320800)   # CMD consecutivos de TU rango
    ... generar modelos con M ...
    c.objective('dv.miobj')                 # dummy por defecto; c.objective('dv.x', 'trigger')
    c.config('minombre', 'Etiqueta en el menú de ajustes', 1)   # -> #minombre dv.cfg, toggle automático
    c.on('second', 'execute if score #minombre dv.cfg matches 1 run function canon:mimod/g/second')
    c.npc('dv_minpc', 'mimod/tick')         # cada tick como el rig (tag dv_npc2)
    c.frames('dv_minpc', 'mimod/frames')    # elige #frame dv.tmp (0 = modelo base del cuerpo)
    c.brain_click('dv_minpc_click', 'zombie', 'dv_minpc', 'mimod/clicked', 'mimod/attacked')
    c.click('dv_mi_objeto', 'mimod/objeto_usado')   # interaction suelta
    c.use_item('mi_item', 'mimod/item/use', cooldown=True)   # carrot_on_a_stick con canon:{id:"mi_item"}
    c.admin('/function canon:admin/mimod/spawn', 'Traer a ...')
    c.sound('mimod.grito', [{'name': 'minecraft:entity.warden.roar', 'type': 'event', 'pitch': 1.4}], 'subtitles.canon.mimod.grito')
    c.text('subtitles.canon.mimod.grito', 'Un grito')
    F('mimod/tick', '''...''')
```

### Ganchos (`c.on(hook, lineas)`)
| hook | contexto |
|---|---|
| `load` | al cargar (`/reload`, inicio). Inicializa fake players con `execute unless score #x dv.dev matches -999999..999999 run ...` |
| `tick` | cada tick, contexto servidor (overworld, spawn) — usa `as`/`at`/`in` |
| `second` | 1 vez por segundo, contexto servidor |
| `player` | cada tick **como cada jugador y en su posición** |
| `npc` (`c.npc`) | cada tick como cada entidad con `dv_npc2` + tu tag, en su posición |
| `click` / `attack` (`c.click`, `c.brain_click`) | como la interaction (`dv_npc_click`); el jugador tiene `dv_talker` |
| `frames` (`c.frames`) | dentro de `rig/visual3`, para rigs con `dv_rigx`: fija `#frame dv.tmp` |
| `die` (`c.die`) | cuando un rig muere (`rig/die`) |
| `luna_notice` | Luna mira alrededor (como Luna): `execute if score @s dv.talkcd matches ..0 if entity @e[tag=X,distance=..16] run function ...` |

`c.patch('ruta/base', fn)` modifica una función existente del mod base (fn: texto -> texto, **idempotente**; preferir *agregar* líneas al final o envolver).

## Sistema de rigs (personajes 3D)

Un personaje = entidad "cerebro" invisible (normalmente `zombie` con `NoAI`, casco para no quemarse) + `item_display` pasajeros con modelos de `leather_horse_armor` + `CustomModelData`.

- `rig_summon(tags, nombre, color, head=True, scale=1.0, health=None, invul=True, base='zombie', ai=False)` → comando summon. Después del summon:
  `execute as @e[type=zombie,tag=dv_new,tag=<tag>,distance=..2,limit=1,sort=nearest] at @s run function canon:<mod>/init`
- En la init: `function canon:rig/init_common` (asigna `dv.id`, invisibilidad, etc.) + `set_cmd('body', CMD['x_idle'])` + `head(CMD['x_cabeza_y'])`.
- Animación: `rig/visual` (base) suma `#frame` al CMD del cuerpo: **modelo = CMD base del cuerpo + frame**. Por eso los modelos de un personaje se registran consecutivos: idle(0), walk_a(1), walk_b(2), ...
- Expresiones: `head(CMD['x_cabeza_risa'])` cambia la cabeza.
- Caminar con tp (NoAI): marca al objetivo con `tag @a[...] add dv_wtgt` y llama `x/walk` (0.16 b/t), `x/walk_slow` (0.12), `x/creep` (0.07), `x/face`. Quitar `dv_xwalk` al inicio de cada tick; `x/walk` lo pone (para la animación de caminar: en tus frames `execute if entity @s[tag=dv_xwalk] ...`).
- Burbuja de texto: `function canon:x/add_bubble` en la init; `x/links_follow` cada tick; `say(...)`/`bubble('dv_xbubble', ...)` para hablar; `x/bubble_clear` cuando `dv.say` llega a 0.
- Clic: en la init `summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","<tu_click_tag>","dv_new_link"],width:0.8f,height:1.95f,response:1b}` y luego `scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id` + `tag @e[tag=dv_new_link] remove dv_new_link`. Registra con `c.brain_click`.
- Mirada: `x/seen` (tag `dv_lookers` a los jugadores) → `#seen dv.tmp`.
- Desaparecer: `function canon:rig/despawn` (limpia todo). `rig/vanish` con humo.
- IA vanilla: `rig_summon(..., ai=True, base='wolf'|'sheep'|...)` para animales que caminan solos (como Luna=wolf, gato=cave_spider, cuervo=chicken, rata=endermite).
- Escala: `scale=1.6` para criaturas grandes (la traslación se ajusta sola).

### Modelos (`canon/models.py`)
- `Atlas(nombre, seed)`: textura 256×256 en `canon:item/modelo/<nombre>`. `Part(atlas, nombre, from, to, color, paint=fn)`: caja con su región de textura (sombreado automático: luz arriba, sombra abajo, borde).
- `humanoid_parts(at, colores, build='normal'|'chubby'|'thin')`, `head_parts(at, colores, 'short'|'emo'|'bob'|'bald')`, `face_rect` + `face_element(at, r, piel, estilo, nombre)` con estilos de `draw_face` (ojos normal/closed/red/wide/angry/void/glow; boca smile/flat/open/laugh/scream/grin/frown/o/none; blush, tears, emo_fringe).
- `pose(P, 'idle'|'walk_a'|'walk_b'|'reach'|'arms_up'|'dance_a'|'dance_b'|'laugh'|'offer'|'float', extra={parte: (angulo, eje, origen)})`. Ángulos válidos: -45, -22.5, 0, 22.5, 45. Coordenadas entre -16 y 32.
- Cuerpo: pies en y=-14, cuello y≈9. Cabeza (modelo aparte): y 8..14.4, la cara mira al **norte** (z bajo).
- `write_model(nombre, textura, elementos)`; `atlas.save()`.
- Vista previa: `python3 tools/preview.py /tmp/x.png kevin_idle+kevin_cabeza_neutral alto_idle` (lee build/out; compila antes).
- Puedes crear tus propias funciones de dibujo/partes en tu módulo. **No cambies** firmas de `canon/models.py` (solo el módulo `remodel` puede AGREGAR funciones ahí).

### Ítems
- Clic derecho: base `carrot_on_a_stick` + `canon:{id:"x"}` + `c.use_item('x', 'mod/x/use')`.
- Modelo de ítem: escribe `assets/canon/models/item/<x>.json` (con `c.json`) y la textura png en `assets/canon/textures/item/<x>.png` (con PIL, ruta `c.path('assets/canon/textures/item/x.png')`), y registra `c.item_model('carrot_on_a_stick', CMD, 'canon:item/x')`.
- Loot table para darlo: `c.json('data/canon/loot_tables/items/x.json', loot_item('carrot_on_a_stick', item_nbt(...)))` y `loot give @s loot canon:items/x`.
- Recetas: en 1.20.1 el resultado no puede tener NBT → receta que da `minecraft:knowledge_book` + logro con criterio `minecraft:recipe_crafted` (`{"recipe_id":"canon:x"}`) cuya recompensa (función) hace `clear @s knowledge_book 1`, da el ítem real con loot y `advancement revoke @s only canon:...`. (Ver módulo herramientas.)
- Muebles: el mod base usa `item_frame` con `EntityTag:{Tags:["dv_place","dv_place_x"]}`; al colocarse, `furn/place` (base) convierte en display + interaction. Para muebles nuevos: `c.patch('furn/place', ...)` agregando una línea `execute if entity @s[tag=dv_place_<x>] run function canon:<mod>/place_<x>` ANTES de `kill @s` (o agregar al principio).

### Sonidos
- Eventos nuevos: `c.sound('mod.evento', [...], 'subtitles.canon....')` + `c.text(subtitulo, 'texto')`.
- Pueden apuntar a **eventos vanilla** (`{'name': 'minecraft:entity.warden.heartbeat', 'type': 'event', 'pitch': 0.8, 'volume': 0.6}`) — se validan contra el registro — o a ogg propios (`canon:mod/archivo` en `assets/canon/sounds/mod/archivo.ogg`, que copias en build desde `tools/assets/<mod>/`).
- Solo el módulo `sonidos` reemplaza (`replace=True`) sonidos existentes del mod base.

## Rangos de CustomModelData (NO salirse del tuyo)

Rigs (`leather_horse_armor`) — base usa 7319999 y 7320000..7320114; 2.1 usa 7320115..7320150 (kevin, nicolas, fiesteros, miron, alto, masa).

| módulo | rigs (leather_horse_armor) | ítems (otros ítems vanilla) | carpetas de funciones |
|---|---|---|---|
| core | — | — | x/, extra/, npc2/, rig/frames/extra |
| remodel | reemplaza modelos base (mismos nombres); extras 7320200–7320299 | — | remodel/ |
| kevin | 7320300–7320399 (+ 2.1 fijos) | 7312100–7312149 | kevin/, alto/, masa/, admin/kevin/ |
| nicolas / miron | 7320400–7320499 | 7312150–7312199 | nicolas/, miron/, mina/ |
| diana | 7320500–7320599 | 7311600–7311649 | diana2/, admin/diana2/ |
| juli (+casa, dani) | 7320600–7320699 | 7311650–7311699 | juli2/, casa/, dani/ |
| luna | 7320700–7320799 | 7311700–7311749 | luna2/ |
| pueblo (NPCs) | 7320800–7321199 | 7311750–7311849 | town2/, pueblo/, npc/ |
| animales | 7321200–7321399 | 7311900–7311949 | animal/ |
| objetos | 7321400–7321599 | 7311000–7311499 | obj/, furn2/ |
| juegos | 7321600–7321699 | 7311850–7311899 | juego/ |
| zombies | 7321700–7321799 | 7311950–7311999 | zomb/ |
| lore (+director) | 7321800–7321899 | 7311500–7311599 | lore/, director/ |
| herramientas (+cámara) | 7321900–7321999 | 7312000–7312099 | herr/, camara/ |
| sonidos | — | — | sonido/ |

## Convenciones compartidas (para coordinarse sin llamarse)

- **Personas** (NPC humanos con rig): tag `dv_humano` + `dv_npc_<nombre>`. Diana-doppelganger puede imitar a cualquier `dv_humano`.
- **Horrores** (criaturas peligrosas): tag `dv_horror`. Luna ladra a `dv_horror` cercanos; los NPC humanos huyen de ellos.
- **Animales** del mod: tag `dv_animal`.
- **Evento canónico del día** (lo elige el director del módulo lore):
  `#canon_ev dv.dev` = id del evento activo (0 = ninguno), `#canon_t dv.dev` = ticks desde que empezó.
  Cada módulo reacciona a SU id (si no está activo, no hace nada):
  | id | evento | quién reacciona |
  |---|---|---|
  | 1 | Luna de sangre (zombis listos y fuertes) | zombies |
  | 2 | La niebla (niebla espesa, susurros) | lore |
  | 3 | La noche de Diana | diana |
  | 4 | Visita de Dani | juli |
  | 5 | La fiesta de Kevin | kevin |
  | 6 | La noche del Mirón | nicolas/miron |
  | 7 | Derrumbe en la mina | nicolas/miron |
  | 8 | La migración (animales raros) | animales |
  | 9 | Feria de Valle Quieto | pueblo |
  | 10 | El gran escondite | juegos |
  | 11 | Luna inquieta (Luna presiente algo) | luna |
  | 12 | Apagón (sin luz, solo linternas y la cámara) | herramientas |
  | 13 | Visita de la Devota | lore |
- **Fake players globales**: usa prefijo de tu módulo (`#di_...`, `#lu_...`) para no chocar. Temporales `#k #c #r #id dv.tmp` se pueden pisar entre funciones (no guardar estado ahí).
- Jugador objetivo de un rig: guardar su `dv.pid` (base asigna uno único por jugador) en `dv.target` del rig.

## Mod base: piezas útiles (en base/data/canon/functions)
- `util/spot_search` (posición segura cerca: `#ok dv.tmp`, marker `dv_spot`), `diana/ground` (bajar/subir al suelo), `travel/store_return` + `util/tp_return` (guardar/volver posición del jugador), `fx/shake_big`, `fx/shake_small`, `hud/peek`.
- Predicados: `en_superficie` (overworld), `en_pueblo`, `en_sueno`, `de_dia`, `de_noche`, `oscuro`, `iluminado`, `agachado`, `corriendo`, `supervivencia`, `visitable`, `azar/*`, `mano/*`.
- Ruido del jugador: `dv.noise` (0 quieto … 5 disparo) calculado cada tick en `player/noise`.
- Scores: `dv.pid` (id jugador), `dv.id` (id rig), `dv.say`, `dv.timer`, `dv.timer2`, `dv.state`, `dv.mode`, `dv.anim`, `dv.frame`, `dv.cmd`, `dv.target`, `dv.watch`, `dv.talkcd`.
- Reloj: `#t #m2 #m4 #m10 #m20 #m40 #m200 dv.clock`.
- Ajustes globales: `#susto dv.cfg` (jumpscares con imagen), `#diana`, `#juli`, `#devota`, `#luna`, `#kevin`, `#nicolas`, `#suenos`, `#vago`, `#clima`, `#flip` (orientación de modelos).
- Font de sustos `canon:susto`:  grito,  torcida,  ojos,  viñeta,  blanco,  negro,  pétalos,  párpado,  viñeta roja.
