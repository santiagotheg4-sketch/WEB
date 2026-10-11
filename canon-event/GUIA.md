# Canon Event 2.1.0 — lo nuevo

Mod para **Minecraft 1.20.1 con Forge**. Pon `canon-event-2.1.0-1.20.1.jar` en la carpeta `mods`, tú y Juan (y en el servidor, si usan uno). Borra el `canon-event-2.0.0` y el `devocion` viejos. Lo mejor es empezar un mundo nuevo.

Menú del mod: `/trigger dv.menu set 1`. Los comandos de prueba (operador) están en el menú, en **Comandos**.

## Kevin
Aparece cerca de ti en el mundo normal: moreno, pelo corto, camisa negra estampada, pantalón negro y tenis. Te sigue, te cuenta chistes y baila. **Clic derecho** para hablar: chiste, ¿qué hacemos hoy?, ¿cómo estás?, baila, ¿tienes algo para mí? (un regalo por día) y chao.

Sus aventuras van en orden:
1. **Fiesta techno** (de noche): luces, fiesteros bailando y música. Kevin te ofrece un vaso: si lo tomas, alucinas. Luego la música se corta, todos te miran y aparece el Mirón.
2. **El bosque** (de noche y dentro de un bosque): busca las 6 notas antes de que el Alto te agarre. Si lo miras mucho tiempo, se te tira encima. Cada nota lo vuelve más rápido.
3. **Las catacumbas**: un laberinto bajo tierra. Busca la llave, abre la reja y sal. La Masa los persigue atravesando las paredes.
4. **Los 3 días**: Kevin no sale de las catacumbas. Pasan tres días de juego sin él. De noche, algo con su cara te llama, y no es él.
5. **Kevin chistoso**: vuelve más gracioso que nunca y puedes repetir cualquier aventura.

## Nicolás y la mina
- Bajo la altura 40, Nicolás (chico gordito, emo, pelo negro corto, ropa negra) puede aparecer detrás de ti. Te persigue, te dice cosas feas y te pega. Subir a la superficie lo espanta, y si lo matas se deshace en humo.
- Al picar piedra o pizarra, de vez en cuando aparece su cara gritando «¡MALDITO!» en el hueco que acabas de picar.

## El Mirón
Una figura negra y flaca, con ojos blancos, que aparece a lo lejos mirándote, en lugares diferentes y con sonido creepy. Si la miras fijo o te acercas, desaparece, y a veces grita. Luna ladra y avisa. En el pueblo aparece más seguido.

## La casa blanca (sueño de los demás)
A veces, si duermes y no eres Santi, sueñas con la casa de madera de dos pisos, rodeada de blanco infinito. Tiene reja, escalones que suben desde la izquierda hasta la puerta, la escalera al segundo piso a la derecha, la cocina, un cuarto a la izquierda y el salón al frente, con el sofá gris y la tele. Por la derecha del salón se sale al jardín. Arriba hay tres puertas y en el techo dos ventanas que se abren y se cierran.

Juli va cambiando de cuarto, hablando y haciendo cosas. Clic derecho para conversar; hay una misión de una foto perdida. Si te alejas mucho de la casa, despiertas.

## Valle Quieto
Ahora pasan cosas de la nada: el Mirón al fondo de la calle, teléfonos sonando en casas vacías, apagones, susurros, la gente del pueblo que se queda mirándote, risas y cuervos.

## Ajustes
En el menú de ajustes puedes apagar a Kevin, a Nicolás y la mina, los sueños en la casa de Juli y el Mirón.

## Tu canción del bosque
Para cambiar la música del bosque por tu MP3, conviértelo a `.ogg` y ponlo en un paquete de recursos en `assets/canon/sounds/music/bosque.ogg`. Lo mismo para el grito de Nicolás: `assets/canon/sounds/nicolas/maldito.ogg`.

## Para desarrolladores
`tools/build.sh` genera los modelos (`tools/gen_models.py`) y la lógica (`tools/gen_functions.py`), revisa todo (`tools/check.py`) y arma el .jar en `build/`.
