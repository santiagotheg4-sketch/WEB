# Canon Event 3.0.0 — guía

Mod para **Minecraft 1.20.1 con Forge**. Pon `canon-event-3.0.0-1.20.1.jar` en la carpeta `mods`, tú y Juan (y Bana), y en el servidor si usan uno. Borra las versiones viejas (`canon-event-2.x` y `devocion`). Lo mejor es empezar un mundo nuevo.

- Menú del mod: `/trigger dv.menu set 1`. Ahí están los **ajustes**, para prender o apagar cada sistema, y los **comandos** de prueba para operadores.
- Todo lo de antes sigue igual: la Devota, Valle Quieto, Mariana, Diana la Zunga, Juli y El Sueño, Kevin, Nicolás, el Mirón y la casa blanca.

## Lo nuevo de la 3.0

### Herramientas que se craftean
Las recetas aparecen en tu libro de recetas.
- **Martillo 3x3**: tres bloques de hierro o diamante arriba y dos palos abajo. Rompe 3x3 de piedra.
- **Excavadora 3x3**: un bloque arriba y dos palos. Cava 3x3 de tierra y arena.
- **Hacha taladora**: dos bloques arriba, un bloque y un palo en la segunda fila, y un palo abajo. Cortas un tronco y cae el árbol entero.
- **Versión de netherita**: igual que la de diamante, pero con un lingote de netherita en la receta.
- **Agachado** rompes un solo bloque, como siempre. Las herramientas gastan durabilidad por cada bloque.

### Cámara instantánea
- **Receta**: hierro, vidrio y redstone.
- **Película**: 2 papeles, pólvora y tinta. Con cada receta salen 4 rollos.
- **Uso**: clic derecho para sacar una foto. Te da la foto con lo que salió en ella, y a veces sale algo que no estaba.
- **El flash** espanta al Mirón, al Alto y a la Zunga, y desenmascara a los **dobles de Diana**.

### Diana
- **Diana humana** (de día): una chica pálida, con ojeras, que pregunta por **Juan**. A **Santiago** le pide que le lleve una carta a Juan.
- **No le mientas**: si le dices que viste a Juan, esa noche te visita.
- **Bana**: Diana lo encuentra de día y le dice «**Te encontré, Bana. Hoy te visito en la noche.**» Esa noche lo visita: golpes, su nombre, pasos, ella detrás, ella gateando y un susto final. Reconoce el usuario `Bana` o `bana`.
- **Dobles**: Diana se pone la cara REAL de uno de ustedes y se para a lo lejos. Si te acercas, se tuerce y grita. En el pueblo también imita a los vagabundos.
- **Luna** les ladra a los dobles.
- **Apariciones nuevas**:
  - al borde de la vista: desaparece si la miras;
  - colgada del techo en las cuevas;
  - junto a tu cama, con «Te vi dormir»;
  - llamadas que dicen tu nombre.

### Dani, la hermana de Juli
Aparece de vez en cuando a lo lejos, mirando. Si la miras o te acercas, te dice que **Juli estaba preguntando por Santi**. Tiene conversaciones con varios temas y te regala una carta de Juli y un pétalo. A veces aparece en el jardín de la casa blanca del sueño.

### Luna
- **Posiciones nuevas**: echada, dar la pata, reverencia, pidiendo en dos patas, aullar, olfatear y cavar.
- **Trucos**: haz clic en Luna con un **palo** en la mano, o usa `/trigger dv.luna set 99`. Puede sentarse, echarse, dar la pata, rodar, ponerse panza arriba, hacerse la muerta, saltar, hacer la reverencia, aullar, pedir y buscar.
- **Sola**: olfatea, cava, se echa de noche y aúlla en luna llena.

### Zombis inteligentes
- **Te oyen**: si caminas o corres, vienen hacia donde hiciste ruido. Agachado no te oyen.
- **Se avisan entre ellos**: el **zombi gritón** llama a la horda.
- **Te alcanzan**: si te subes a algo, ponen bloques y suben. Si se atascan, rompen bloques débiles como tierra, vidrio, hojas o lana.
- **Variantes**:
  - **corredor**: rápido;
  - **tanque**: con mucha vida y armadura;
  - **minero**: rompe piedra;
  - y uno que se queda quieto hasta que te acercas.
- De noche son más rápidos.

### Eventos canónicos
Desde el día 2, algunas noches y algunos días empieza un **EVENTO CANÓNICO**, anunciado en pantalla:
- **Luna de sangre**: más zombis, y más fuertes.
- **La niebla**.
- **La noche de Diana**.
- **La noche del Mirón**.
- **Apagón**: la cámara es clave.
- **Visita de Dani** (de día).

### Escondite entre ustedes
`/trigger dv.juego set 1` (cualquiera puede empezarlo). Uno busca y queda ciego 30 segundos. Los demás se esconden y tienen 3 minutos. Si el buscador llega a 2 bloques de alguien, lo encuentra. Cada 30 segundos, los escondidos suenan.

### NPCs nuevos
- **En Valle Quieto**: Don Ernesto el sepulturero, Rosa la panadera, el Padre Tomás (te bendice), el Policía Ramírez, Sofi la niña que no crece, Wilson el del radio, Toño el mecánico (te explica cómo escapar) y Lucía la mesera.
- **En el mundo normal**: Don Aurelio el viajero (te regala un boleto) y Marta la leñadora.
- Cada uno tiene sus temas de conversación (clic derecho), un regalo y su propia historia, y se asustan con los monstruos.

## Tu música
Para usar tu propia música o voces, conviértelas a `.ogg` (mono para voces y efectos) y ponlas en un paquete de recursos con la misma ruta:
- música del bosque: `assets/canon/sounds/music/bosque.ogg`;
- grito de Nicolás: `assets/canon/sounds/nicolas/maldito.ogg`.

## Para desarrolladores
- `python3 tools/build.py` arma el .jar en `build/`: toma `base/` (el mod original), le suma todos los módulos de `tools/features/` y lo verifica todo (sintaxis oficial con `mecha` y registros de 1.20.1).
- Arquitectura: `docs/ARQUITECTURA.md`. Historia: `docs/LORE.md`.
