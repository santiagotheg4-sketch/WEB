"""Mariana (nuevo papel) y la Abuela. Personajes con forma de jugador y skin 64x64 (canon/skins.py).

MARIANA: chica inexpresiva obsesionada con su ex (Felipe). No se le puede hablar: si insistes,
se enoja («Nunca me vuelvas a hablar») y desde ahí te acecha: aparece y desaparece, te mira y te deja
carteles cerca de tu casa. Si le das una flor, te perdona (o eso parece). Busca a Felipe: deja carteles.
ABUELA CARMEN: aparece al anochecer cerca de bosques. Te ofrece sopita, habla de sus nietos que se
fueron al bosque, te invita a su casa... si la sigues a la oscuridad, gatea detrás de ti.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as S

MC = '#b0a6b8'
AC = '#c9a27a'
MARI = dict(skin='#ead6c8', hair='#1c1416', hair_style='long', eyes='#2a2024', top='#2b2b33', top_style='long', pants='#1c1c22',
            pants_style='skirt', tights='#2a2630', shoes='#141414', lips='#9a6a70', extras=['dark_circles', 'necklace'])
ABU = dict(skin='#d8b8a0', hair='#d8d8d8', hair_style='bun', eyes='#3a3028', brows='#bdbdbd', top='#5a3a4a', top_style='cardigan',
           top2='#7a5a6a', pants='#4a3a40', pants_style='long_dress', shoes='#2a2020', lips='#8a5a5a', extras=['glasses', 'shawl', 'apron'],
           shawl='#6a4a3a')
MARI_POSES = ('idle', 'walk_a', 'walk_b', 'reach', 'point')
MARI_EXPR = ('neutral', 'angry', 'creepy')
ABU_POSES = ('idle', 'walk_a', 'walk_b', 'reach', 'run_a')
ABU_EXPR = ('smile', 'creepy', 'scared')


def build(c):
    shim.use(c)
    mb, mh = S.build_character('mariana2', MARI, c.out, MARI_POSES, MARI_EXPR)
    ab, ah = S.build_character('abuela', ABU, c.out, ABU_POSES, ABU_EXPR)
    shim.models(mb + mh, 7321000)
    shim.models(ab + ah, 7321010)
    K = shim.CMD
    c.config('mariana2', 'Mariana (acecha si le hablas)', 1)
    c.config('abuela', 'La abuela Carmen', 1)
    c.objective('dv.abu', 'trigger')
    for o in ('dv.mari', 'dv.mcd2'):
        c.objective(o)
    for n in (12, 40):
        c.const(n)
    c.on('load', '''
execute unless score #ma_cd dv.dev matches -999999..999999 run scoreboard players set #ma_cd dv.dev 600
execute unless score #ab_cd dv.dev matches -999999..999999 run scoreboard players set #ab_cd dv.dev 900
''')
    c.on('player', 'scoreboard players enable @s dv.abu\nexecute if score @s dv.abu matches 1.. run function canon:abuela/eleccion')
    c.on('second', '''
execute if score #ma_cd dv.dev matches 1.. run scoreboard players remove #ma_cd dv.dev 1
execute if score #ab_cd dv.dev matches 1.. run scoreboard players remove #ab_cd dv.dev 1
scoreboard players remove @a[scores={dv.mcd2=1..}] dv.mcd2 1
execute if score #mariana2 dv.cfg matches 1 if score #ma_cd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_mari2] as @a[gamemode=!spectator,limit=1,sort=random] at @s if predicate canon:visitable if predicate canon:azar/1en500 run function canon:mari2/aparecer
execute if score #mariana2 dv.cfg matches 1 if score #ma_cd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_mari2] as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en400 run function canon:mari2/aparecer
execute if score #mariana2 dv.cfg matches 1 as @a[tag=dv_mari_odio,gamemode=!spectator,predicate=canon:en_superficie] at @s unless score @s dv.mcd2 matches 1.. if predicate canon:azar/1en120 run function canon:mari2/acecho
execute if score #abuela dv.cfg matches 1 if score #ab_cd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_abuela] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:visitable if predicate canon:azar/1en500 run function canon:abuela/aparecer
''')
    c.npc('dv_mari2', 'mari2/tick')
    c.npc('dv_abuela', 'abuela/tick')
    c.frames('dv_mari2', 'mari2/frames')
    c.frames('dv_abuela', 'abuela/frames')
    c.brain_click('dv_mari2_click', 'zombie', 'dv_mari2', 'mari2/clic', 'mari2/golpe')
    c.brain_click('dv_abuela_click', 'zombie', 'dv_abuela', 'abuela/clic', 'abuela/golpe')

    def rig(prefix, tag, name, color, click):
        F(f'{prefix}/summon', rig_summon([tag, 'dv_humano'], name, color) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag={tag},distance=..2,limit=1,sort=nearest] at @s run function canon:{prefix}/init')
        return (f'summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","{click}","dv_new_link"],width:0.8f,height:1.9f,response:1b}}\n'
                'scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id\ntag @e[tag=dv_new_link] remove dv_new_link\nfunction canon:x/add_bubble')

    # ============================================================== MARIANA
    inter = rig('mari2', 'dv_mari2', 'Mariana', MC, 'dv_mari2_click')
    F('mari2/init', f'''
function canon:rig/init_common
{set_cmd('body', K['mariana2_idle'])}
{head(K['mariana2_cabeza_neutral'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.state 0
{inter}
''')
    F('mari2/aparecer', '''
scoreboard players set #ma_cd dv.dev 1200
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:mari2/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('mari2/tick', '''
function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..40,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:mari2/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('mari2/piensa', '''
execute if score @s dv.state matches 0 run function canon:mari2/busca
execute if score @s dv.state matches 1 run function canon:mari2/acecha
execute if score @s dv.timer matches 1800.. run function canon:mari2/irse
''')
    # buscando a Felipe: camina lento, se detiene, mira alrededor, a veces deja un cartel
    F('mari2/busca', '''
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #200 dv.math
execute if score #c dv.tmp matches 1 run tp @s ~ ~ ~ ~70 0
execute if score #c dv.tmp matches 1..60 if block ^ ^ ^0.6 #canon:pasable run function canon:mari2/paso
execute if score #c dv.tmp matches 100 if entity @a[tag=dv_wtgt,distance=..12] run function canon:x/face
execute if score #c dv.tmp matches 150 if predicate canon:azar/1en3 run function canon:mari2/cartel_felipe
''')
    c.const(200)
    F('mari2/paso', 'tag @s add dv_xwalk\ntp @s ^ ^ ^0.06\nexecute at @s run function canon:diana/ground')
    c.pick('mari2/cartel_felipe', [
        f'setblock ~ ~ ~ minecraft:oak_sign[rotation=0]{{front_text:{{messages:[\'{jt("FELIPE", "black")}\',\'{jt("vuelve", "black")}\',\'{jt("te espero", "black")}\',\'{jt("donde siempre", "black")}\']}}}} keep',
        f'setblock ~ ~ ~ minecraft:oak_sign[rotation=4]{{front_text:{{messages:[\'{jt("SE BUSCA", "dark_red")}\',\'{jt("Felipe", "black")}\',\'{jt("si lo ves", "black")}\',\'{jt("no le digas", "black")}\']}}}} keep',
        f'setblock ~ ~ ~ minecraft:oak_sign[rotation=8]{{front_text:{{messages:[\'{jt("el me dijo", "black")}\',\'{jt("que volvia", "black")}\',\'{jt("mintio", "dark_red")}\',\'{jt("", "black")}\']}}}} keep',
    ])
    F('mari2/acecha', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches 8.. run function canon:mari2/esfumarse
execute if entity @a[tag=dv_wtgt,distance=..4] run function canon:mari2/esfumarse
execute if score @s dv.timer matches 400.. run function canon:mari2/esfumarse
''')
    F('mari2/esfumarse', '''
particle minecraft:ash ~ ~1 ~ 0.4 0.9 0.4 0 30 normal
playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 0.6 0.6
execute if predicate canon:azar/50 as @a[tag=dv_wtgt] at @s run function canon:mari2/cartel_odio
function canon:rig/despawn
''')
    F('mari2/irse', 'particle minecraft:ash ~ ~1 ~ 0.4 0.9 0.4 0 30 normal\nfunction canon:rig/despawn')
    c.pick('mari2/cartel_odio_txt', [
        f'setblock ~ ~ ~ minecraft:spruce_sign[rotation=0]{{front_text:{{messages:[\'{jt("TE DIJE", "dark_red")}\',\'{jt("que no me", "black")}\',\'{jt("hablaras", "black")}\',\'{jt("", "black")}\']}}}} keep',
        f'setblock ~ ~ ~ minecraft:spruce_sign[rotation=0]{{front_text:{{messages:[\'{jt("te estoy", "black")}\',\'{jt("mirando", "dark_red")}\',\'{jt("", "black")}\',\'{jt("- M", "black")}\']}}}} keep',
        f'setblock ~ ~ ~ minecraft:spruce_sign[rotation=0]{{front_text:{{messages:[\'{jt("el tampoco", "black")}\',\'{jt("me hablaba", "black")}\',\'{jt("mira como", "black")}\',\'{jt("termino", "dark_red")}\']}}}} keep',
        f'setblock ~ ~ ~ minecraft:spruce_sign[rotation=0]{{front_text:{{messages:[\'{jt("NUNCA", "dark_red")}\',\'{jt("ME VUELVAS", "dark_red")}\',\'{jt("A HABLAR", "dark_red")}\',\'{jt("", "black")}\']}}}} keep',
    ])
    F('mari2/cartel_odio', '''
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:mari2/cartel_odio_txt
kill @e[type=marker,tag=dv_spot]
''')
    # clic: no habla. Si insistes, se enoja.
    F('mari2/clic', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if entity @a[tag=dv_talker,limit=1,nbt={{SelectedItem:{{id:"minecraft:poppy"}}}}] run function canon:mari2/flor
execute unless entity @a[tag=dv_talker,limit=1,nbt={{SelectedItem:{{id:"minecraft:poppy"}}}}] run function canon:mari2/insistir
''')
    F('mari2/insistir', f'''
scoreboard players operation #id dv.tmp = @s dv.id
scoreboard players add @a[tag=dv_talker] dv.mari 1
execute if entity @a[tag=dv_talker,scores={{dv.mari=1}}] run {bubble('dv_xbubble', '...', MC, 50).splitlines()[1]}
execute if entity @a[tag=dv_talker,scores={{dv.mari=1}}] run scoreboard players set @s dv.say 50
execute if entity @a[tag=dv_talker,scores={{dv.mari=2}}] run tellraw @a[tag=dv_talker] {jt('Mariana te mira sin parpadear. No dice nada.', 'gray', True)}
execute if entity @a[tag=dv_talker,scores={{dv.mari=3}}] run function canon:mari2/no_me_hables
execute if entity @a[tag=dv_talker,scores={{dv.mari=4..}}] run function canon:mari2/enojo
''')
    F('mari2/no_me_hables', head(K['mariana2_cabeza_angry']) + '\n' + say('Mariana', MC, '#efe8f2', 'No me hables.', 70, '@a[tag=dv_talker]'))
    F('mari2/enojo', f'''
{head(K['mariana2_cabeza_creepy'])}
''' + say('Mariana', MC, '#efe8f2', 'Nunca. Me vuelvas. A hablar.', 90, '@a[distance=..16]') + '''
tag @a[tag=dv_talker] add dv_mari_odio
scoreboard players set @a[tag=dv_talker] dv.mari 0
scoreboard players add @a[tag=dv_talker] dv.miedo 20
playsound canon:diana.scream hostile @a[tag=dv_talker] ~ ~ ~ 0.5 1.6
execute as @a[tag=dv_talker] run function canon:fx/shake_small
scoreboard players set @s dv.state 2
scoreboard players set @s dv.timer 1790
''')
    F('mari2/flor', '''
clear @a[tag=dv_talker] minecraft:poppy 1
tag @a[tag=dv_talker] remove dv_mari_odio
scoreboard players set @a[tag=dv_talker] dv.mari 0
tellraw @a[tag=dv_talker] {"text":"Mariana toma la flor sin mirarte. La aprieta hasta que se deshace. Se va.","color":"#b0a6b8","italic":true}
scoreboard players set @s dv.timer 1790
''')
    F('mari2/golpe', 'function canon:mari2/enojo')
    # acecho de Mariana para quien le habló demasiado
    F('mari2/acecho', '''
scoreboard players set @s dv.mcd2 100
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute if predicate canon:azar/50 positioned ^8 ^ ^10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-6 ^ ^-9 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:mari2/summon_acecho
kill @e[type=marker,tag=dv_spot]
execute if score @s dv.home matches 1 if predicate canon:azar/1en3 run function canon:mari2/cartel_odio
''')
    F('mari2/summon_acecho', '''
function canon:mari2/summon
execute as @e[type=zombie,tag=dv_mari2,distance=..2,limit=1,sort=nearest] run function canon:mari2/modo_acecho
''')
    F('mari2/modo_acecho', f'''
scoreboard players set @s dv.state 1
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.watch 0
tag @s add dv_horror
{head(K['mariana2_cabeza_creepy'])}
''')
    F('mari2/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if score @s dv.state matches 1 run scoreboard players set #frame dv.tmp 4
''')

    # ============================================================== ABUELA CARMEN
    inter = rig('abuela', 'dv_abuela', 'Abuela Carmen', AC, 'dv_abuela_click')
    F('abuela/init', f'''
function canon:rig/init_common
{set_cmd('body', K['abuela_idle'])}
{head(K['abuela_cabeza_smile'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.state 0
{inter}
''')
    F('abuela/aparecer', '''
scoreboard players set #ab_cd dv.dev 1500
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:abuela/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('abuela/tick', '''
function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..40,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:abuela/piensa
tag @a remove dv_wtgt
''')
    F('abuela/piensa', '''
execute if score @s dv.state matches 0 run function canon:abuela/espera
execute if score @s dv.state matches 1 run function canon:abuela/guia
execute if score @s dv.state matches 2 run function canon:abuela/persigue
execute if score @s dv.state matches 3 run function canon:abuela/se_va
''')
    F('abuela/espera', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
execute if entity @a[tag=dv_wtgt,distance=..8] if score @s dv.say matches ..0 if score #m200 dv.clock matches 40 run function canon:abuela/llama
execute if score @s dv.timer matches 2400.. run scoreboard players set @s dv.state 3
''')
    c.pick('abuela/llama', [say('Abuela Carmen', AC, '#f6ead8', t, 110) for t in [
        'Ven, mijito. Te hice sopita. Está calientica.', '¿Tienes frío? Ven, que la abuela te abriga.',
        'Mis nietos jugaban por aquí. Se fueron al bosque. Ya van a volver.', 'Qué ojitos tan bonitos tienes. Los quiero para mí. Es un decir.',
        '¿Ya comiste? Tienes cara de no haber comido. Ven.']])
    menu_ab = menu('@a[tag=dv_talker]', 'ABUELA CARMEN', AC, [('Aceptar sopita', '/trigger dv.abu set 1'), ('¿Vive sola?', '/trigger dv.abu set 2'),
                                                            ('¿Y sus nietos?', '/trigger dv.abu set 3'), ('Acompañarla a su casa', '/trigger dv.abu set 4'),
                                                            ('Me tengo que ir', '/trigger dv.abu set 5')])
    F('abuela/clic', f'execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0\nscoreboard players set @s dv.timer 0\n{menu_ab}')
    F('abuela/golpe', f'{head(K["abuela_cabeza_creepy"])}\n' + say('Abuela Carmen', AC, '#f6ead8', 'Ay, mijito. Eso no se le hace a la abuela. Ahora sí te voy a encontrar.', 90) +
      '\nscoreboard players set @s dv.state 2\nscoreboard players set @s dv.timer 0')
    F('abuela/eleccion', '''
tag @s add dv_atalk
scoreboard players operation #ac dv.tmp = @s dv.abu
scoreboard players set @s dv.abu 0
execute as @e[type=zombie,tag=dv_abuela,distance=..12,limit=1,sort=nearest] at @s run function canon:abuela/responde
tag @s remove dv_atalk
''')
    F('abuela/responde', '''
execute if score #ac dv.tmp matches 1 run function canon:abuela/sopa
execute if score #ac dv.tmp matches 2 run function canon:abuela/r2
execute if score #ac dv.tmp matches 3 run function canon:abuela/r3
execute if score #ac dv.tmp matches 4 run function canon:abuela/r4
execute if score #ac dv.tmp matches 5 run function canon:abuela/r5
''')
    c.pick('abuela/sopa', [
        say('Abuela Carmen', AC, '#f6ead8', 'Tómatela toda. Así, así. Qué bien.', 90) + '\nloot give @a[tag=dv_atalk] loot canon:items/sopa\neffect give @a[tag=dv_atalk] minecraft:regeneration 8 0 true',
        say('Abuela Carmen', AC, '#f6ead8', 'Tómatela toda. ¿Sabe raro? Es la receta de la casa.', 90) + '\neffect give @a[tag=dv_atalk] minecraft:nausea 10 0 true\neffect give @a[tag=dv_atalk] minecraft:poison 4 0 true',
        say('Abuela Carmen', AC, '#f6ead8', 'Para el camino. Y no le hagas caso a la muchacha pálida.', 90) + '\nloot give @a[tag=dv_atalk] loot canon:items/pizza',
    ])
    F('abuela/r2', say('Abuela Carmen', AC, '#f6ead8', 'Sola no, mijito. Con los que se quedan. Siempre se quedan. Tú también te vas a quedar.', 130))
    F('abuela/r3', f'{head(K["abuela_cabeza_creepy"])}\n' + say('Abuela Carmen', AC, '#f6ead8', 'Se fueron al bosque. Los llamo todas las noches. A veces contestan. Con otra voz.', 140))
    F('abuela/r4', say('Abuela Carmen', AC, '#f6ead8', 'Sígueme, que la casa queda cerquita. Por aquí. Por lo oscuro.', 100) + '\nscoreboard players set @s dv.state 1\nscoreboard players set @s dv.timer 0')
    F('abuela/r5', say('Abuela Carmen', AC, '#f6ead8', 'Vuelve pronto. Siempre vuelven.', 80) + '\nscoreboard players set @s dv.state 3\nscoreboard players set @s dv.timer 0')
    # la abuela guía hacia lo oscuro; si la sigues lejos, se transforma
    F('abuela/guia', '''
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~180 0 if block ^ ^ ^0.7 #canon:pasable positioned ^ ^ ^0.08 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
tag @s add dv_xwalk
execute if score @s dv.timer matches 200.. if entity @a[tag=dv_wtgt,distance=..10] run function canon:abuela/transformar
execute if score @s dv.timer matches 200.. unless entity @a[tag=dv_wtgt,distance=..10] run scoreboard players set @s dv.state 3
''')
    F('abuela/transformar', f'''
{head(K['abuela_cabeza_creepy'])}
scoreboard players set @s dv.state 2
scoreboard players set @s dv.timer 0
tag @s add dv_horror
playsound canon:devota.scream hostile @a[distance=..24] ~ ~ ~ 1 0.6
''' + say('Abuela Carmen', AC, '#f6ead8', 'Ya llegamos, mijito. Esta es mi casa. Y tú eres mi nieto nuevo.', 100))
    F('abuela/persigue', '''
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.2 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
tag @s add dv_xwalk
execute if score #m10 dv.clock matches 0 run playsound canon:diana.crawl hostile @a[distance=..20] ~ ~ ~ 1 1.2
execute if entity @a[tag=dv_wtgt,distance=..1.5] run function canon:abuela/atrapa
execute if score @s dv.timer matches 400.. run scoreboard players set @s dv.state 3
''')
    F('abuela/atrapa', '''
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
damage @a[tag=dv_wtgt,limit=1] 6 minecraft:mob_attack by @s
playsound canon:devota.scream master @a[tag=dv_wtgt] ~ ~ ~ 1 0.8
scoreboard players set @s dv.state 3
''')
    F('abuela/se_va', 'particle minecraft:ash ~ ~1 ~ 0.4 0.9 0.4 0 30 normal\nfunction canon:rig/despawn')
    F('abuela/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if score @s dv.state matches 2 run scoreboard players set #frame dv.tmp 4
''')
    F('admin/pers/mariana', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^6 run function canon:mari2/summon')
    F('admin/pers/mariana_acecho', 'tag @s add dv_mari_odio\nscoreboard players set @s dv.mcd2 0\nfunction canon:mari2/acecho')
    F('admin/pers/abuela', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^6 run function canon:abuela/summon')
    c.admin('/function canon:admin/pers/mariana', 'Traer a Mariana')
    c.admin('/function canon:admin/pers/mariana_acecho', 'Mariana te acecha (como si la hubieras enojado)')
    c.admin('/function canon:admin/pers/abuela', 'Traer a la abuela Carmen')
