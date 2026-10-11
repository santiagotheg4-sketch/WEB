"""Dani, la hermana de Juli. Aparece de vez en cuando a lo lejos, mirando.
Si la miras o te acercas, habla: Juli estaba preguntando por Santi. Menú de diálogo,
regalos y una aparición en el jardín de la casa blanca del sueño. Evento canónico 4.
"""
import json
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import models as M
from canon.ctx import item_nbt, loot_item

DC = '#9fc3a8'


def dsay(text, ticks=110, sel='@a[distance=..20]'):
    return say('Dani', DC, '#e3f1e6', text, ticks, sel)


def models():
    at = M.Atlas('dani', 601)
    skin = '#e9cdb9'

    def hoodie(a, f, r):
        x, y, w, h = r
        if f == 'north':
            M.rect(a, x + w // 2 - 3, y + h - 7, 6, 4, '#3f5a49')       # bolsillo canguro
            M.px(a, x + w // 2 - 2, y + 1, '#e8e8e8')
            M.px(a, x + w // 2 + 1, y + 1, '#e8e8e8')                    # cordones
            M.rect(a, x + w // 2 - 2, y + 2, 1, 4, '#e8e8e8')
            M.rect(a, x + w // 2 + 1, y + 2, 1, 4, '#e8e8e8')

    def sleeve(a, f, r):
        x, y, w, h = r
        M.rect(a, x, y + h - 3, w, 3, skin)
        M.rect(a, x, y + h - 5, w, 2, '#3f5a49')

    def jeans(a, f, r):
        x, y, w, h = r
        for i in range(0, w, 3):
            M.px(a, x + i, y + h // 2, '#56708f')

    def shoes(a, f, r):
        x, y, w, h = r
        M.rect(a, x, y + h - 2, w, 2, '#d8d8d8')
    c = dict(skin=skin, pants='#3e5677', shoes='#f0f0f0', belt='#2a2a2e', shirt='#4d6b58', sleeve='#4d6b58',
             shirt_paint=hoodie, arm_paint=sleeve, leg_paint=jeans, shoe_paint=shoes, arm_w=2.3, wide_shoulders=0.15)
    P = M.humanoid_parts(at, c)
    for n in ['idle', 'walk_a', 'walk_b', 'reach']:
        M.write_model('dani_' + n, 'dani', M.pose(P, n))
    M.write_model('dani_brazos', 'dani', M.pose(P, 'idle', {'arm_r': (45, 'x', M.ARM_O_R), 'arm_l': (45, 'x', M.ARM_O_L)}))
    at.save()
    ah = M.Atlas('dani_cabeza', 602)
    hair = '#2b1d17'
    H = M.head_parts(ah, dict(skin=skin, hair=hair), 'short')
    hs = lambda a, f, r: M.hair_strands(a, f, r)
    H['hair_back'] = M.Part(ah, 'hair_back', [4.6, 9.6, 10.5], [11.4, 14.6, 11.4], hair, paint=hs)
    H['coleta'] = M.Part(ah, 'coleta', [7.0, 3.5, 11.2], [9.0, 12.0, 12.6], hair, paint=hs)       # cola de caballo
    H['liga'] = M.Part(ah, 'liga', [6.8, 11.0, 11.0], [9.2, 11.8, 12.8], '#7a2f3b')
    H['fringe'] = M.Part(ah, 'fringe', [8.2, 12.6, 4.6], [11.1, 14.2, 4.95], hair, paint=hs)
    base = dict(iris='#3a2618', brow='#2b1d17', lips='#b56c70')
    exprs = {'seria': dict(base, mouth='flat'), 'preocupada': dict(base, mouth='frown'),
             'triste': dict(base, mouth='frown', tears=True), 'sonrisa': dict(base, mouth='smile', blush='#e2aca4')}
    for n, st in exprs.items():
        r = M.face_rect(ah)
        fe = M.face_element(ah, r, skin, st, 'face_' + n)
        M.write_model('dani_cabeza_' + n, 'dani_cabeza', M.all_elements(H) + [fe])
    ah.save()


NAMES = ['dani_idle', 'dani_walk_a', 'dani_walk_b', 'dani_reach', 'dani_brazos',
         'dani_cabeza_seria', 'dani_cabeza_preocupada', 'dani_cabeza_triste', 'dani_cabeza_sonrisa']


def build(c):
    shim.use(c)
    shim.models(NAMES, 7320620)
    models()
    from canon import skins as SK
    SK.build_character('dani', dict(skin='#e9cdb9', hair='#2b1d17', hair_style='ponytail', eyes='#3a2618', top='#4d6b58', top_style='hoodie',
                                    pants='#3e5677', shoes='#f0f0f0', lips='#b56c70', extras=['freckles']), c.out,
                       ('idle', 'walk_a', 'walk_b', 'reach', 'brazos'),
                       [('seria', 'flat'), ('preocupada', 'sad'), ('triste', 'cry'), ('sonrisa', 'smile')])
    K = shim.CMD
    c.config('dani', 'Dani, la hermana de Juli', 1)
    c.objective('dv.dani', 'trigger')
    for n in (12, 40, 200):
        c.const(n)
    c.on('load', 'execute unless score #da_cd dv.dev matches -999999..999999 run scoreboard players set #da_cd dv.dev 900')
    c.on('player', 'scoreboard players enable @s dv.dani\nexecute if score @s dv.dani matches 1.. run function canon:dani/eleccion')
    c.on('second', '''
execute if score #da_cd dv.dev matches 1.. run scoreboard players remove #da_cd dv.dev 1
execute if score #dani dv.cfg matches 1 run function canon:dani/g/second
execute unless score #dani dv.cfg matches 1 as @e[type=zombie,tag=dv_dani] at @s run function canon:rig/despawn
''')
    F('dani/g/second', '''
execute if score #da_cd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_dani] as @a[gamemode=!spectator,predicate=canon:de_dia,limit=1,sort=random] at @s if predicate canon:visitable if predicate canon:azar/1en600 run function canon:dani/aparecer
execute if score #da_cd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_dani] as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en600 run function canon:dani/aparecer
execute if score #canon_ev dv.dev matches 4 unless score #da_ev dv.dev matches 1 unless entity @e[type=zombie,tag=dv_dani] as @a[gamemode=!spectator,predicate=canon:de_dia,limit=1,sort=random] at @s if predicate canon:azar/1en20 run function canon:dani/visita_evento
execute unless score #canon_ev dv.dev matches 4 run scoreboard players set #da_ev dv.dev 0
execute unless entity @e[type=zombie,tag=dv_dani] as @a[predicate=canon:en_casa_sueno,limit=1,sort=random] if predicate canon:azar/1en400 run function canon:dani/en_la_casa
''')
    c.npc('dv_dani', 'dani/tick')
    c.frames('dv_dani', 'dani/frames')
    c.brain_click('dv_dani_click', 'zombie', 'dv_dani', 'dani/clic', 'dani/golpe')
    F('dani/summon', rig_summon(['dv_dani', 'dv_humano'], 'Dani', DC) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_dani,distance=..2,limit=1,sort=nearest] at @s run function canon:dani/init')
    F('dani/init', f'''
function canon:rig/init_common
{set_cmd('body', K['dani_idle'])}
{head(K['dani_cabeza_seria'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.state 0
scoreboard players set @s dv.say -1
scoreboard players set @s dv.watch 0
summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","dv_dani_click","dv_new_link"],width:0.8f,height:1.95f,response:1b}}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
function canon:x/add_bubble
''')
    F('dani/aparecer', '''
scoreboard players set #da_cd dv.dev 1500
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^6 ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:dani/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('dani/visita_evento', 'scoreboard players set #da_ev dv.dev 1\nscoreboard players set #da_cd dv.dev 0\nfunction canon:dani/aparecer\n'
      'title @s times 10 60 20\ntitle @s subtitle {"text":"Alguien te está esperando afuera.","color":"#9fc3a8","italic":true}\ntitle @s title {"text":" "}')
    F('dani/en_la_casa', '''
scoreboard players set #da_cd dv.dev 600
scoreboard players operation #pid dv.tmp = @s dv.pid
execute in canon:sueno_blanco positioned -5.5 64 3.5 run function canon:dani/summon
tellraw @s {"text":"Por la ventana del salón se ve a alguien en el jardín. No es Juli.","color":"#9fc3a8","italic":true}
''')
    F('dani/tick', f'''
function canon:x/links_follow
scoreboard players remove @s[scores={{dv.say=1..}}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..40,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:dani/irse_ya
execute if entity @a[tag=dv_wtgt] run function canon:dani/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('dani/piensa', '''
execute unless score @s dv.state matches 2 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.state matches 0 run function canon:x/seen
execute if score @s dv.state matches 0 if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.state matches 0 if score @s dv.watch matches 30.. run function canon:dani/habla_primero
execute if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=..9] run function canon:dani/habla_primero
execute if score @s dv.state matches 0 if score @s dv.timer matches 700.. run function canon:dani/se_va_ya
execute if score @s dv.state matches 1 if entity @a[tag=dv_wtgt,distance=5..] if entity @a[tag=dv_wtgt,distance=..9] run function canon:x/walk_slow
execute if score @s dv.state matches 1 if score #m200 dv.clock matches 60 if score @s dv.say matches ..0 run function canon:dani/charla
execute if score @s dv.state matches 1 if score @s dv.timer matches 2400.. run function canon:dani/se_va_ya
execute if score @s dv.state matches 2 run function canon:dani/se_va
''')
    F('dani/habla_primero', '''
scoreboard players set @s dv.state 1
scoreboard players set @s dv.timer 0
execute if entity @a[tag=dv_wtgt,tag=dv_santi] run function canon:dani/hola_santi
execute unless entity @a[tag=dv_wtgt,tag=dv_santi] run function canon:dani/hola_otro
tellraw @a[tag=dv_wtgt] {"text":"(Clic derecho en Dani para hablar con ella.)","color":"gray","italic":true}
''')
    F('dani/hola_santi', head(K['dani_cabeza_preocupada']) + '\n' + dsay('Santi. Juli estaba preguntando por ti. Otra vez. No deja de soñar contigo.', 150))
    pick('dani/hola_otro', [dsay(t, 140) for t in [
        'Hola. Soy Dani, la hermana de Juli. Ella estaba preguntando por Santi. ¿Tú lo conoces?',
        'Perdón que te mire tanto. Juli estaba preguntando por Santi y pensé que eras él.',
        'Juli estaba preguntando por Santi otra vez. Dice que lo ve en una casa blanca. ¿Le dices?',
    ]])
    pick('dani/charla', [dsay(t, 120) for t in [
        'Juli duerme demasiado. Cada día un poco más.',
        'Anoche habló dormida. Dijo: Santi, la puerta está ahí.',
        'Yo también soñé con esa casa. Con la escalera a la derecha. Qué raro, ¿no?',
        'Si ves a una chica pálida preguntando por Juan, no le contestes. Yo no le contesto.',
        'Mi hermana dibuja flores rosadas en todo. Dice que la protegen.',
        'No le cuentes a Juli que vine. Se pone triste cuando sabe que me preocupo.',
    ]])
    F('dani/se_va_ya', dsay('Ya me voy. Cuídate. Y cuida a Santi.', 60) + '\nscoreboard players set @s dv.state 2\nscoreboard players set @s dv.timer2 0')
    F('dani/se_va', '''
tag @s add dv_xwalk
scoreboard players add @s dv.timer2 1
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~180 0 positioned ^ ^ ^0.14 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
execute if score @s dv.timer2 matches 90.. run function canon:dani/irse_ya
''')
    F('dani/irse_ya', 'particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.8 0.4 0 20 normal\nfunction canon:rig/despawn')
    F('dani/golpe', head(K['dani_cabeza_triste']) + '\n' + dsay('Oye. ¿Qué te pasa? Con razón Juli prefiere soñar.', 80) +
      '\nscoreboard players set @s dv.state 2\nscoreboard players set @s dv.timer2 0')
    F('dani/clic', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set @s dv.state 1
scoreboard players set @s dv.timer 0
{menu('@a[tag=dv_talker]', 'DANI', DC, [('¿Cómo está Juli?', '/trigger dv.dani set 1'), ('¿Qué es la casa blanca?', '/trigger dv.dani set 2'),
                                        ('¿Por qué me mirabas?', '/trigger dv.dani set 3'), ('¿Juli va a despertar?', '/trigger dv.dani set 4'),
                                        ('Háblame de ti', '/trigger dv.dani set 7'), ('Adiós', '/trigger dv.dani set 6')])}
{menu('@a[tag=dv_talker,tag=dv_santi]', '', DC, [('¿Qué te dijo Juli de mí?', '/trigger dv.dani set 5')])}
''')
    F('dani/eleccion', '''
tag @s add dv_datalk
scoreboard players operation #dac dv.tmp = @s dv.dani
scoreboard players set @s dv.dani 0
execute unless entity @e[type=zombie,tag=dv_dani,distance=..12] run tellraw @s {"text":"Dani ya no está.","color":"gray","italic":true}
execute as @e[type=zombie,tag=dv_dani,distance=..12,limit=1,sort=nearest] at @s run function canon:dani/responde
tag @s remove dv_datalk
''')
    R = {
        1: ('dani_cabeza_preocupada', 'Duerme. Mucho. Cuando despierta sonríe como si viniera de un lugar bonito. Y pregunta por Santi.'),
        2: ('dani_cabeza_seria', 'Una casa de madera en un blanco que no termina. La sueñan los que duermen cerca de Santi. Juli vive ahí cuando duerme.'),
        3: ('dani_cabeza_sonrisa', 'Perdón. Es que Juli me describe a la gente de sus sueños. Y tú te pareces a uno.'),
        4: ('dani_cabeza_triste', 'No sé. Si Santi la encuentra en el sueño de las flores, a lo mejor sí. A lo mejor por eso lo busca tanto.'),
        5: ('dani_cabeza_sonrisa', 'Que te ríes raro. Que tienes un perrito negro que se llama Luna. Y que le prometiste algo. No me dijo qué.'),
        7: ('dani_cabeza_seria', 'Soy la hermana mayor. La que se queda despierta. Alguien tiene que estar despierta, ¿no?'),
    }
    lines = []
    for k, (hd, t) in R.items():
        F(f'dani/r{k}', head(K[hd]) + '\n' + dsay(t, 160, '@a[distance=..16]'))
        lines.append(f'execute if score #dac dv.tmp matches {k} run function canon:dani/r{k}')
    lines += ['execute if score #dac dv.tmp matches 6 run function canon:dani/se_va_ya',
              'execute if score #dac dv.tmp matches 1..5 unless entity @a[tag=dv_datalk,tag=dv_dani_regalo] run function canon:dani/regalo']
    F('dani/responde', '\n'.join(lines))
    F('dani/regalo', '''
tag @a[tag=dv_datalk] add dv_dani_regalo
loot give @a[tag=dv_datalk] loot canon:dani/carta_juli
loot give @a[tag=dv_datalk] loot canon:items/petalo
tellraw @a[tag=dv_datalk] {"text":"Dani: Toma. Juli escribió esto dormida. Creo que es para Santi. Y un pétalo: los de ella protegen.","color":"#e3f1e6","italic":true}
playsound canon:juli.chime ambient @a[tag=dv_datalk] ~ ~ ~ 0.7 1.2
''')
    F('dani/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if score @s dv.state matches 1 unless entity @s[tag=dv_xwalk] run scoreboard players set #frame dv.tmp 4
''')
    pages = ['Santi:\n\nAquí siempre está a punto de amanecer. No sé cuánto tiempo llevo. Dani dice que mucho.',
             'Hay una casa blanca donde los otros sueñan conmigo. Les pregunto por ti. Nadie sabe.\n\nLuna me ladra en sueños. Es buena.',
             'Si me buscas, sigue los pétalos. Y no le hables a la chica que pregunta por Juan.\n\nJ.']
    pages_s = ','.join("'" + json.dumps({'text': txt(p.replace(chr(10), ' NL '))}, ensure_ascii=False).replace(' NL ', chr(92) * 2 + 'n') + "'" for p in pages)
    c.json('data/canon/loot_tables/dani/carta_juli.json', loot_item('written_book', item_nbt(
        'carta_juli2', 'Carta de Juli (escrita dormida)', '#f2a7c3', ['Te la dio Dani.', 'La letra se pone rosada con la luz.'], None,
        f'title:"Para Santi",author:"Juli",pages:[{pages_s}]')))
    F('admin/dani/traer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^10 run function canon:dani/summon')
    F('admin/dani/aparecer', 'scoreboard players set #da_cd dv.dev 0\nfunction canon:dani/aparecer')
    c.admin('/function canon:admin/dani/traer', 'Traer a Dani (cerca)')
    c.admin('/function canon:admin/dani/aparecer', 'Dani aparece a lo lejos mirando')
