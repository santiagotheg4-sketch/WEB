"""Diana (ampliación): Diana humana, la obsesión con Bana y las visitas nocturnas,
los dobles (doppelgänger con la cara real de un jugador o copiando a un NPC) y
apariciones nuevas de la Zunga (borde de la vista, techo de cuevas, cama, llamadas).
Usa los modelos base de Diana (CMD 7320078..7320093) para la Zunga.
"""
import json
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import models as M
from canon.ctx import item_nbt, loot_item

DH = '#cdb8c8'   # color de Diana humana
DIANA_BODY, DIANA_HEAD_GRIN, DIANA_HEAD_SCREAM, DIANA_HEAD_CRAWL, DIANA_NECK = 7320078, 7320088, 7320089, 7320091, 7320093


def dsay(text, ticks=100, sel='@a[distance=..20]'):
    return say('Diana', DH, '#f0e4ec', text, ticks, sel)


# ------------------------------------------------------------------ modelos
def models():
    at = M.Atlas('diana_humana', 501)
    skin = '#efe2dc'

    def dress(a, f, r):
        x, y, w, h = r
        if f == 'north':
            for i in range(0, w, 4):
                M.px(a, x + i, y + 2, '#d9cfc6')
            M.rect(a, x + w // 2 - 1, y, 2, 3, skin)

    def sleeve(a, f, r):
        x, y, w, h = r
        M.rect(a, x, y + h - 3, w, 3, skin)
    c = dict(skin=skin, pants=skin, shoes='#3a2c2a', belt='#cfc4ba', shirt='#ece4d8', sleeve='#e4dccf',
             skirt='#e8dfd2', shirt_paint=dress, arm_paint=sleeve, arm_w=2.0)
    P = M.humanoid_parts(at, c)
    P['skirt'] = M.Part(at, 'skirt', [4.0, -9.5, 5.6], [12.0, 0.2, 10.4], '#e8dfd2', faces=['north', 'south', 'east', 'west', 'down'])
    for n in ['idle', 'walk_a', 'walk_b', 'reach']:
        M.write_model('dhumana_' + n, 'diana_humana', M.pose(P, n))
    at.save()
    ah = M.Atlas('diana_humana_cabeza', 502)
    hair = '#141012'
    H = M.head_parts(ah, dict(skin=skin, hair=hair), 'short')
    hs = lambda a, f, r: M.hair_strands(a, f, r)
    H['hair_back'] = M.Part(ah, 'hair_back', [4.4, 2.0, 10.4], [11.6, 14.6, 11.8], hair, paint=hs)
    H['hair_l'] = M.Part(ah, 'hair_l', [3.9, 3.0, 5.0], [5.0, 14.4, 11.6], hair, paint=hs)
    H['hair_r'] = M.Part(ah, 'hair_r', [11.0, 3.0, 5.0], [12.1, 14.4, 11.6], hair, paint=hs)
    H['fringe'] = M.Part(ah, 'fringe', [5.0, 12.8, 4.6], [9.0, 14.2, 4.95], hair, paint=hs)
    base = dict(iris='#1b1214', brow='#141012', lips='#b48a8a', blush=None)

    def ojeras(a, r):
        x, y, w, h = r
        ey = y + int(h * 0.45) + 2
        for ex in (x + int(w * 0.22), x + int(w * 0.62)):
            M.rect(a, ex, ey, max(3, int(w * 0.17)), 1, '#a88f9c')
    exprs = {'amable': dict(base, mouth='smile'), 'triste': dict(base, mouth='frown', tears=True),
             'seria': dict(base, mouth='flat'), 'glitch': dict(base, eyes='void', mouth='grin')}
    for n, st in exprs.items():
        r = M.face_rect(ah)
        st = {k: v for k, v in st.items() if v is not None}
        fe = M.face_element(ah, r, skin, st, 'face_' + n)
        if n != 'glitch':
            ojeras(ah, r)
        M.write_model('dhumana_cabeza_' + n, 'diana_humana_cabeza', M.all_elements(H) + [fe])
    ah.save()
    # cuerpo del doble (ropa genérica de jugador; la cabeza es la cabeza real del jugador)
    ad = M.Atlas('doble', 503)
    cd = dict(skin='#c8a58a', pants='#2b3550', shoes='#2a2a2a', belt='#1f1f24', shirt='#3b5f7a', sleeve='#3b5f7a')
    PD = M.humanoid_parts(ad, cd)
    M.write_model('doble_idle', 'doble', M.pose(PD, 'idle'))
    M.write_model('doble_walk_a', 'doble', M.pose(PD, 'walk_a'))
    M.write_model('doble_walk_b', 'doble', M.pose(PD, 'walk_b'))
    M.write_model('doble_twist', 'doble', M.pose(PD, 'idle', {'arm_r': (45, 'z', M.ARM_O_R), 'arm_l': (45, 'z', M.ARM_O_L),
                                                               'leg_r': (-22.5, 'z', M.LEG_O), 'shoe_r': (-22.5, 'z', M.LEG_O)}))
    ad.save()


HUMANA = ['dhumana_idle', 'dhumana_walk_a', 'dhumana_walk_b', 'dhumana_reach',
          'dhumana_cabeza_amable', 'dhumana_cabeza_triste', 'dhumana_cabeza_seria', 'dhumana_cabeza_glitch',
          'doble_idle', 'doble_walk_a', 'doble_walk_b', 'doble_twist']


def book(title, pages):
    pj = ','.join("'" + json.dumps(json.dumps({'text': p}, ensure_ascii=False))[1:-1].replace("'", "\\'") + "'" for p in pages)
    return pj


def written_book_loot(path, item_id, name, color, title, author, pages, lore):
    pages_s = ','.join("'" + json.dumps({'text': txt(p.replace(chr(10), ' NL '))}, ensure_ascii=False).replace(' NL ', chr(92) * 2 + 'n') + "'" for p in pages)
    nbt = item_nbt(item_id, name, color, lore, None, f'title:"{title}",author:"{author}",pages:[{pages_s}]')
    C.json(path, loot_item('written_book', nbt))


C = None


def build(c):
    global C
    C = c
    shim.use(c)
    shim.models(HUMANA, 7320500)
    models()
    from canon import skins as SK
    SK.build_character('dhumana', dict(skin='#efe2dc', hair='#141012', hair_style='long', eyes='#1b1214', top='#ece4d8', top_style='long',
                                       pants='#e8dfd2', pants_style='long_dress', shoes='#3a2c2a', lips='#b48a8a', extras=['dark_circles']), c.out,
                       ('idle', 'walk_a', 'walk_b', 'reach'), [('amable', 'smile'), ('triste', 'cry'), ('seria', 'flat'), ('glitch', 'glitch')])
    K = shim.CMD
    c.config('diana_humana', 'Diana humana (pregunta por Juan)', 1)
    c.config('diana_visitas', 'Visitas nocturnas de Diana (y a Bana)', 1)
    c.config('doppel', 'Dobles de Diana (doppelgänger)', 1)
    for o in ('dv.dhr',):
        c.objective(o, 'trigger')
    for o in ('dv.dvis', 'dv.dzz', 'dv.dvcd'):
        c.objective(o)
    for n in (2, 4, 10, 12, 20, 40, 60):
        c.const(n)
    c.on('load', '''
execute unless score #di_hcd dv.dev matches -999999..999999 run scoreboard players set #di_hcd dv.dev 600
execute unless score #di_zcd dv.dev matches -999999..999999 run scoreboard players set #di_zcd dv.dev 300
execute unless score #di_dcd dv.dev matches -999999..999999 run scoreboard players set #di_dcd dv.dev 1500
execute unless score #di_bana dv.dev matches -999999..999999 run scoreboard players set #di_bana dv.dev 0
execute unless score #di_bday dv.dev matches -999999..999999 run scoreboard players set #di_bday dv.dev 0
''')
    c.on('player', '''
scoreboard players enable @s dv.dhr
execute if score @s dv.dhr matches 1.. run function canon:diana2/humana/eleccion
execute if entity @s[name=Bana] run tag @s add dv_bana
execute if entity @s[name=bana] run tag @s add dv_bana
execute if score #diana dv.cfg matches 1 if score #diana_visitas dv.cfg matches 1 if entity @s[tag=dv_di_visita] if predicate canon:de_noche if predicate canon:en_superficie run function canon:diana2/visita/tick
execute if data entity @s SleepingX run scoreboard players add @s dv.dzz 1
execute unless data entity @s SleepingX run scoreboard players set @s dv.dzz 0
execute if score #diana dv.cfg matches 1 if score @s dv.dzz matches 45 if predicate canon:azar/1en5 run function canon:diana2/zunga/cama
''')
    c.on('second', '''
execute if score #di_hcd dv.dev matches 1.. run scoreboard players remove #di_hcd dv.dev 1
execute if score #di_zcd dv.dev matches 1.. run scoreboard players remove #di_zcd dv.dev 1
execute if score #di_dcd dv.dev matches 1.. run scoreboard players remove #di_dcd dv.dev 1
scoreboard players remove @a[scores={dv.dvcd=1..}] dv.dvcd 1
execute if score #diana dv.cfg matches 1 run function canon:diana2/g/second
execute unless score #diana dv.cfg matches 1 as @e[type=zombie,tag=dv_d2rig] at @s run function canon:rig/despawn
''')
    F('diana2/g/second', '''
# Diana humana (de día)
execute if score #diana_humana dv.cfg matches 1 if score #di_hcd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_dhum] as @a[gamemode=!spectator,predicate=canon:de_dia,limit=1,sort=random] at @s if predicate canon:visitable if predicate canon:azar/1en400 run function canon:diana2/humana/aparecer
# Bana: Diana lo encuentra de día
execute if score #diana_visitas dv.cfg matches 1 if score #di_bana dv.dev matches 0 unless entity @e[type=zombie,tag=dv_dhum] as @a[tag=dv_bana,gamemode=!spectator,predicate=canon:de_dia,limit=1] at @s if predicate canon:visitable if predicate canon:azar/1en250 run function canon:diana2/bana/aparecer
execute if score #di_bana dv.dev matches 2 run function canon:diana2/bana/enfriar
# la Zunga en lugares nuevos
execute if score #di_zcd dv.dev matches ..0 as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche] at @s if predicate canon:azar/1en600 run function canon:diana2/zunga/borde
execute if score #di_zcd dv.dev matches ..0 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @s[y=-64,dy=112] if predicate canon:azar/1en600 run function canon:diana2/zunga/techo
execute as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche] at @s if predicate canon:azar/1en1500 run function canon:diana2/llamada
# La noche de Diana (evento canónico 3): mucho más activa
execute if score #canon_ev dv.dev matches 3 if score #di_zcd dv.dev matches ..0 as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche] at @s if predicate canon:azar/1en150 run function canon:diana2/zunga/borde
execute if score #canon_ev dv.dev matches 3 as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche,tag=!dv_di_visita] at @s if predicate canon:azar/1en600 run tag @s add dv_di_visita
# dobles
execute if score #doppel dv.cfg matches 1 if score #di_dcd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_doppel] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en1200 run function canon:diana2/doble/intentar
execute if score #doppel dv.cfg matches 1 if score #di_dcd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_doppel] as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en300 run function canon:diana2/doble_npc/intentar
''')
    c.npc('dv_dhum', 'diana2/humana/tick')
    c.npc('dv_zunga', 'diana2/zunga/tick')
    c.npc('dv_doppel', 'diana2/doble/tick')
    c.frames('dv_dhum', 'diana2/humana/frames')
    c.frames('dv_zunga', 'diana2/zunga/frames')
    c.frames('dv_doppel', 'diana2/doble/frames')
    c.brain_click('dv_dhum_click', 'zombie', 'dv_dhum', 'diana2/humana/clic', 'diana2/humana/golpe')
    c.brain_click('dv_dnpc_click', 'zombie', 'dv_doppel', 'diana2/doble/descubierto', 'diana2/doble/descubierto')
    c.on('luna_notice', 'execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_doppel,distance=..24] run function canon:luna/alarm_watch')
    c.on('luna_notice', 'execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_zunga,distance=..24] run function canon:luna/alarm_watch')

    # ============================================================== DIANA HUMANA
    F('diana2/humana/summon', rig_summon(['dv_dhum', 'dv_d2rig', 'dv_humano'], 'Diana', DH) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_dhum,distance=..2,limit=1,sort=nearest] at @s run function canon:diana2/humana/init')
    F('diana2/humana/init', f'''
function canon:rig/init_common
{set_cmd('body', K['dhumana_idle'])}
{head(K['dhumana_cabeza_amable'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players operation @s dv.state = #dstate dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.talk 0
scoreboard players set @s dv.timer2 0
summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","dv_dhum_click","dv_new_link"],width:0.8f,height:1.95f,response:1b}}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
function canon:x/add_bubble
particle minecraft:ash ~ ~1 ~ 0.4 0.8 0.4 0 20 normal
''')
    F('diana2/humana/aparecer', '''
scoreboard players set #di_hcd dv.dev 1500
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 0
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^4 ^ ^-10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/humana/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('diana2/humana/tick', f'''
function canon:x/links_follow
scoreboard players remove @s[scores={{dv.say=1..}}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
scoreboard players remove @s[scores={{dv.timer2=1..}}] dv.timer2 1
execute if score @s dv.timer2 matches 0 if entity @s[tag=dv_dglitch] run function canon:diana2/humana/glitch_fin
tag @a remove dv_wtgt
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:diana2/humana/irse_ya
execute if entity @a[tag=dv_wtgt] run function canon:diana2/humana/piensa
tag @a remove dv_wtgt
''')
    F('diana2/humana/piensa', '''
execute unless score @s dv.state matches 2 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=3.5..] run function canon:x/walk_slow
execute if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=..3.5] run function canon:diana2/humana/saluda
execute if score @s dv.state matches 1 if score #m200 dv.clock matches 120 if score @s dv.say matches ..0 run function canon:diana2/humana/charla
execute if score @s dv.state matches 2 run function canon:diana2/humana/se_va
execute if score @s dv.state matches 3 run function canon:diana2/bana/mira
execute if score @s dv.state matches 0..1 if score @s dv.timer matches 2400.. run function canon:diana2/humana/despedida
execute unless score @s dv.state matches 2 if predicate canon:de_noche run function canon:diana2/humana/noche
''')
    F('diana2/humana/saluda', '''
scoreboard players set @s dv.state 1
execute if entity @a[tag=dv_wtgt,tag=dv_santi] run function canon:diana2/humana/saluda_santi
execute if entity @a[tag=dv_wtgt,tag=dv_bana,tag=!dv_santi] run function canon:diana2/humana/saluda_bana
execute unless entity @a[tag=dv_wtgt,tag=dv_santi] unless entity @a[tag=dv_wtgt,tag=dv_bana] run function canon:diana2/humana/saluda_otro
tellraw @a[tag=dv_wtgt] {"text":"(Clic derecho en ella para hablar.)","color":"gray","italic":true}
''')
    F('diana2/humana/saluda_santi', dsay('Santiago... por fin. ¿Has visto a Juan? Tú eres su amigo. Tú sabes dónde está.', 140))
    F('diana2/humana/saluda_bana', dsay('Bana. Te estaba buscando. Bueno, a ti no. A Juan. ¿Lo has visto?', 130))
    pick('diana2/humana/saluda_otro', [dsay(t, 120) for t in [
        'Hola. Perdón que te moleste... ¿tú conoces a Juan?',
        'Disculpa. Estoy buscando a alguien. Se llama Juan. Me prometió volver.',
        'Hola. Qué bonito día, ¿no? ¿Has visto a Juan por aquí?',
    ]])
    pick('diana2/humana/charla', [dsay(t, 110) for t in [
        'Juan siempre llegaba tarde. Pero siempre llegaba.',
        'Llevo mucho tiempo sin dormir. Si duermo, me olvidan.',
        'Ese chico, Santiago, sabe algo. Lo noto en cómo me mira.',
        'A veces me miro en el agua y no me reconozco.',
        'Bana me cae bien. Huele a miedo. Es bonito.',
        '¿Por qué nadie dice mi nombre completo? Díganlo. Por favor.',
        'Si ves a Juan, no le digas que estoy así. Dile que estoy bien.',
    ]])
    F('diana2/humana/despedida', dsay('Ya me tengo que ir. Nos vemos. Siempre nos vemos.', 80) + '\nscoreboard players set @s dv.state 2\nscoreboard players set @s dv.timer2 0')
    F('diana2/humana/se_va', '''
tag @s add dv_xwalk
scoreboard players add @s dv.timer2 1
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~180 0 positioned ^ ^ ^0.12 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
execute if score @s dv.timer2 matches 100.. run function canon:diana2/humana/irse_ya
''')
    F('diana2/humana/irse_ya', '''
particle minecraft:ash ~ ~1 ~ 0.4 0.9 0.4 0 30 normal
function canon:rig/despawn
''')
    F('diana2/humana/noche', f'''
{head(K['dhumana_cabeza_glitch'])}
playsound canon:diana.laugh hostile @a[distance=..24] ~ ~ ~ 1 0.8
{chat('Diana', DH, 'Ya es de noche. Ya no tengo que fingir.', '@a[distance=..24]')}
function canon:rig/vanish
''')
    F('diana2/humana/glitch', f'''
{head(K['dhumana_cabeza_glitch'])}
tag @s add dv_dglitch
scoreboard players set @s dv.timer2 14
scoreboard players set @s dv.talk 2
playsound canon:diana.crack hostile @a[distance=..12] ~ ~ ~ 1 0.9
playsound canon:diana.scream hostile @a[distance=..12] ~ ~ ~ 0.35 1.6
execute as @a[tag=dv_talker] run function canon:fx/shake_small
''')
    F('diana2/humana/glitch_fin', f'''
tag @s remove dv_dglitch
{head(K['dhumana_cabeza_amable'])}
''' + dsay('Perdón. Perdón. No dormí bien. ¿De qué hablábamos?', 90))
    F('diana2/humana/golpe', dsay('¿Por qué hiciste eso? Juan nunca me haría eso. Bueno. Una vez.', 90) + '\nfunction canon:diana2/humana/glitch')
    menu_all = menu('@a[tag=dv_talker]', 'DIANA', DH, [
        ('¿Quién es Juan?', '/trigger dv.dhr set 1'), ('No lo he visto', '/trigger dv.dhr set 2'),
        ('Sí, lo vi', '/trigger dv.dhr set 3'), ('¿Quién eres?', '/trigger dv.dhr set 4'),
        ('¿Por qué esas ojeras?', '/trigger dv.dhr set 5'), ('¿Conoces a Bana?', '/trigger dv.dhr set 8'),
        ('Adiós', '/trigger dv.dhr set 7')])
    menu_santi = menu('@a[tag=dv_talker,tag=dv_santi]', '', DH, [('Le diré a Juan que lo buscas', '/trigger dv.dhr set 6')])
    F('diana2/humana/clic', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players add @s dv.talk 1
execute if score @s dv.talk matches 6.. run function canon:diana2/humana/glitch
execute if score @s dv.talk matches ..5 run {menu_all}
execute if score @s dv.talk matches ..5 run {menu_santi}
''')
    F('diana2/humana/eleccion', '''
tag @s add dv_dtalk
scoreboard players operation #dc dv.tmp = @s dv.dhr
scoreboard players set @s dv.dhr 0
execute unless entity @e[type=zombie,tag=dv_dhum,distance=..12] run tellraw @s {"text":"Diana ya no está.","color":"gray","italic":true}
execute as @e[type=zombie,tag=dv_dhum,distance=..12,limit=1,sort=nearest] at @s run function canon:diana2/humana/responde
tag @s remove dv_dtalk
''')
    resp = {
        1: 'Juan es alguien que me prometió volver. Dijo: espérame aquí. Y yo esperé. Sigo esperando.',
        2: 'Ah. Bueno. Si lo ves, dile que sigo aquí. Que no me he ido. Que no me voy a ir nunca.',
        4: 'Me llamo Diana. Bueno, antes me llamaban así. Ahora nadie dice mi nombre completo. ¿Te diste cuenta?',
        5: 'No duermo. Si duermo, me olvidan. Pedí que nadie me olvidara nunca. Y mira: nadie puede.',
        7: 'Nos vemos. Siempre nos vemos. Aunque tú no me veas a mí.',
        8: 'Bana... sí. Lo estoy buscando también. Tiene algo de Juan en la mirada. Dile que voy a pasar a saludar.',
    }
    lines = []
    for k, t in resp.items():
        F(f'diana2/humana/r{k}', dsay(t, 140, '@a[distance=..16]'))
        lines.append(f'execute if score #dc dv.tmp matches {k} run function canon:diana2/humana/r{k}')
    lines.append('execute if score #dc dv.tmp matches 3 run function canon:diana2/humana/mentira')
    lines.append('execute if score #dc dv.tmp matches 6 if entity @a[tag=dv_dtalk,tag=dv_santi] run function canon:diana2/humana/carta')
    lines.append('execute if score #dc dv.tmp matches 7 run scoreboard players set @s dv.state 2')
    lines.append('execute if score #dc dv.tmp matches 7 run scoreboard players set @s dv.timer2 0')
    F('diana2/humana/responde', '\n'.join(lines))
    F('diana2/humana/mentira', f'''
{head(K['dhumana_cabeza_glitch'])}
tag @s add dv_dglitch
scoreboard players set @s dv.timer2 20
''' + dsay('Mentira. Juan no está. Yo sé cuando mienten. Esta noche hablamos mejor tú y yo.', 140, '@a[distance=..16]') + '''
tag @a[tag=dv_dtalk] add dv_di_visita
playsound canon:diana.name hostile @a[tag=dv_dtalk] ~ ~ ~ 1 0.8
''')
    F('diana2/humana/carta', f'''
{head(K['dhumana_cabeza_triste'])}
''' + dsay('Gracias, Santiago. Toma. Dásela a Juan. Y no la leas. Bueno, si la lees, no me digas.', 160, '@a[distance=..16]') + '''
loot give @a[tag=dv_dtalk] loot canon:diana2/carta_juan
playsound canon:fx.gift neutral @a[distance=..12] ~ ~ ~ 1 1
scoreboard players set @s dv.state 2
scoreboard players set @s dv.timer2 0
''')
    F('diana2/humana/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_dglitch] run scoreboard players set #frame dv.tmp 3
''')

    # ============================================================== BANA
    F('diana2/bana/aparecer', '''
scoreboard players set #di_hcd dv.dev 900
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 3
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^12 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/humana/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run playsound canon:fx.heartbeat ambient @s ~ ~ ~ 0.8 1
''')
    F('diana2/bana/mira', f'''
{head(K['dhumana_cabeza_seria'])}
tag @a remove dv_lookers
tag @a[tag=dv_wtgt] add dv_lookers
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
tag @a remove dv_lookers
execute if score @s dv.watch matches 20.. run function canon:diana2/bana/aviso
execute if score @s dv.timer matches 200.. run function canon:diana2/bana/aviso
execute if entity @a[tag=dv_wtgt,distance=..9] run function canon:diana2/bana/aviso
''')
    F('diana2/bana/aviso', f'''
{head(K['dhumana_cabeza_glitch'])}
title @a[tag=dv_wtgt] times 5 70 20
title @a[tag=dv_wtgt] subtitle {{"text":"Hoy te visito en la noche.","color":"#c94a4a","italic":true}}
title @a[tag=dv_wtgt] title {{"text":"Te encontré, Bana.","color":"#f0e4ec"}}
{chat('Diana', DH, 'Te encontré, Bana. Hoy te visito en la noche.', '@a')}
playsound canon:diana.laugh hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.7
playsound canon:fx.stinger master @a[tag=dv_wtgt] ~ ~ ~ 0.8 0.8
tag @a[tag=dv_wtgt] add dv_di_visita
scoreboard players set #di_bana dv.dev 1
tellraw @a[tag=!dv_bana] {jt('Si ven a Bana esta noche, no lo dejen solo.', 'gray', True)}
function canon:rig/vanish
''')
    F('diana2/bana/enfriar', '''
execute store result score #dday dv.tmp run time query day
execute if score #dday dv.tmp >= #di_bday dv.dev run scoreboard players set #di_bana dv.dev 0
''')

    # ============================================================== VISITA NOCTURNA (jugador con dv_di_visita)
    F('diana2/visita/tick', '''
scoreboard players add @s dv.dvis 1
execute if score @s dv.dvis matches 1 run function canon:diana2/visita/s0
execute if score @s dv.dvis matches 100 run playsound canon:diana.knock hostile @s ^ ^ ^-6 1 1
execute if score @s dv.dvis matches 118 run playsound canon:diana.knock hostile @s ^ ^ ^-6 1 0.95
execute if score @s dv.dvis matches 136 run playsound canon:diana.knock hostile @s ^ ^ ^-6 1 0.9
execute if score @s dv.dvis matches 260 run function canon:diana2/visita/s1
execute if score @s dv.dvis matches 400 run playsound canon:diana.pasos hostile @s ^-4 ^ ^-4 1 1
execute if score @s dv.dvis matches 430 run playsound canon:diana.pasos hostile @s ^4 ^ ^-3 1 0.9
execute if score @s dv.dvis matches 520 run function canon:diana2/visita/s2
execute if score @s dv.dvis matches 640 run playsound canon:fx.heartbeat_fast ambient @s ~ ~ ~ 1 1
execute if score @s dv.dvis matches 700 run function canon:diana2/visita/s3
execute if score @s dv.dvis matches 900 run function canon:diana2/visita/s4
execute if score @s dv.dvis matches 980 run function canon:diana2/visita/fin
''')
    F('diana2/visita/s0', f'''
tellraw @s {jt('Esta noche no estás solo.', '#c94a4a', True)}
playsound canon:diana.breath hostile @s ~ ~ ~ 1 0.8
effect give @s minecraft:darkness 6 0 true
''')
    F('diana2/visita/s1', '''
title @s times 10 40 20
title @s subtitle {"text":"...está aquí.","color":"#c94a4a","italic":true}
title @s title ["",{"selector":"@s","color":"#f0e4ec"}]
playsound canon:diana.name hostile @s ^ ^ ^-3 1 0.9
''')
    F('diana2/visita/s2', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zmode dv.tmp 3
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/zunga/summon
kill @e[type=marker,tag=dv_spot]
playsound canon:diana.flicker hostile @s ~ ~ ~ 1 1
''')
    F('diana2/visita/s3', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zmode dv.tmp 4
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^8 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/zunga/summon
kill @e[type=marker,tag=dv_spot]
playsound canon:diana.crawl hostile @s ^ ^ ^6 1 1
playsound canon:diana.scream hostile @s ^ ^ ^6 0.6 0.8
''')
    F('diana2/visita/s4', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players operation #me dv.tmp = @s dv.pid
execute as @e[type=zombie,tag=dv_zunga] if score @s dv.target = #me dv.tmp at @s run function canon:rig/despawn
scoreboard players set #zmode dv.tmp 5
execute positioned ^ ^ ^-1.4 run function canon:diana2/zunga/summon
playsound canon:diana.jumpscare master @s ~ ~ ~ 1 1
function canon:x/jumpscare
damage @s 4 minecraft:generic
effect give @s minecraft:blindness 2 0 true
''')
    F('diana2/visita/fin', f'''
tag @s remove dv_di_visita
scoreboard players set @s dv.dvis 0
{chat('Diana', DH, 'Mañana vuelvo. O pasado. Tú no sabes cuándo. Yo sí.', '@s')}
loot give @s loot canon:items/mechon
loot give @s loot canon:diana2/diario
execute if entity @s[tag=dv_bana] run function canon:diana2/visita/fin_bana
''')
    F('diana2/visita/fin_bana', '''
scoreboard players set #di_bana dv.dev 2
execute store result score #di_bday dv.dev run time query day
scoreboard players add #di_bday dv.dev 2
''')

    # ============================================================== LA ZUNGA (rig propio con modelos base)
    part = lambda kind, t, s: ('{id:"minecraft:item_display",Tags:["dv_part","dv_%s","dv_cal","dv_rot"],item_display:"none",view_range:1.2f,'
                               'item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}},'
                               'transformation:{translation:[0f,%sf,0f],left_rotation:[0f,0f,0f,1f],scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}}' % (kind, t, s, s, s))
    F('diana2/zunga/summon', 'summon minecraft:zombie ~ ~ ~ {Tags:["dv_brain","dv_npc2","dv_rigx","dv_new","dv_zunga","dv_horror","dv_d2rig"],'
      'CustomName:\'{"text":"Diana","color":"#8a7a86"}\',Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:1b,IsBaby:0b,CanPickUpLoot:0b,'
      'ArmorItems:[{},{},{},{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}}],ArmorDropChances:[0f,0f,0f,0f],'
      'HandDropChances:[0f,0f],DeathLootTable:"canon:vacio",Passengers:[' + ','.join([part('body', 1.4575, 1.06), part('head', 1.5238, 1.06), part('neck', 1.4244, 0)]) + ']}\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_zunga,distance=..2,limit=1,sort=nearest] at @s run function canon:diana2/zunga/init')
    F('diana2/zunga/init', f'''
function canon:rig/init_common
{set_cmd('body', DIANA_BODY)}
{head(DIANA_HEAD_GRIN)}
execute on passengers if entity @s[tag=dv_neck] run scoreboard players set @s dv.cmd {DIANA_NECK}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players operation @s dv.mode = #zmode dv.tmp
scoreboard players set @s dv.watch 0
execute if score @s dv.mode matches 2 on passengers run data merge entity @s {{transformation:{{left_rotation:[0f,0f,1f,0f]}}}}
execute if score @s dv.mode matches 4 run {head(DIANA_HEAD_CRAWL).splitlines()[0]}
execute if score @s dv.mode matches 4 run tag @s add dv_zcrawl
execute if score @s dv.mode matches 1 run tag @s add dv_ztwist
execute if score @s dv.mode matches 5 run {head(DIANA_HEAD_SCREAM).splitlines()[0]}
''')
    F('diana2/zunga/tick', '''
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..32,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:diana2/zunga/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('diana2/zunga/piensa', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.mode matches 1 if score @s dv.watch matches 3.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 1 if score @s dv.timer matches 300.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 2 if score @s dv.watch matches 6.. run function canon:diana2/zunga/techo_grito
execute if score @s dv.mode matches 2 if score @s dv.timer matches 400.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 3 if score @s dv.watch matches 10.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 3 if score @s dv.timer matches 120.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 4 if score #seen dv.tmp matches 0 if entity @a[tag=dv_wtgt,distance=1.6..] run function canon:diana2/zunga/gatea
execute if score @s dv.mode matches 4 if entity @a[tag=dv_wtgt,distance=..1.6] run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 4 if score @s dv.timer matches 220.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 5 if score @s dv.timer matches 14.. run function canon:diana2/zunga/se_esfuma
execute if score @s dv.mode matches 6 if score @s dv.timer matches 60.. run function canon:diana2/zunga/se_esfuma
''')
    F('diana2/zunga/gatea', '''
tag @s add dv_xwalk
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.11 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
execute if score #m20 dv.clock matches 0 run playsound canon:diana.crawl hostile @a[distance=..16] ~ ~ ~ 0.8 1
''')
    F('diana2/zunga/se_esfuma', '''
playsound canon:diana.flicker hostile @a[distance=..24] ~ ~ ~ 1 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 25 normal
function canon:rig/despawn
''')
    F('diana2/zunga/techo_grito', f'''
{head(DIANA_HEAD_SCREAM)}
playsound canon:diana.scream hostile @a[distance=..32] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] run function canon:fx/shake_big
scoreboard players set @s dv.mode 6
scoreboard players set @s dv.timer 0
''')
    F('diana2/zunga/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_ztwist] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 5
execute if entity @s[tag=dv_ztwist] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 6
execute if entity @s[tag=dv_zcrawl] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 7
execute if entity @s[tag=dv_zcrawl] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 8
execute if score @s dv.mode matches 5 run scoreboard players set #frame dv.tmp 3
''')
    F('diana2/zunga/borde', '''
scoreboard players set #di_zcd dv.dev 240
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zmode dv.tmp 1
scoreboard players set #ok dv.tmp 0
execute if predicate canon:azar/1en2 positioned ^9 ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-9 ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/zunga/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run playsound canon:diana.breath hostile @s ~ ~ ~ 0.5 0.9
''')
    F('diana2/zunga/techo', '''
scoreboard players set #di_zcd dv.dev 300
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zmode dv.tmp 2
scoreboard players set #zs dv.tmp 0
scoreboard players set #ok dv.tmp 0
execute anchored eyes positioned ^ ^ ^6 if block ~ ~ ~ #canon:pasable run function canon:diana2/zunga/techo_buscar
''')
    F('diana2/zunga/techo_buscar', '''
scoreboard players add #zs dv.tmp 1
execute unless block ~ ~1 ~ #canon:pasable align y positioned ~ ~-1.83 ~ run function canon:diana2/zunga/techo_poner
execute if score #ok dv.tmp matches 0 if score #zs dv.tmp matches ..7 if block ~ ~1 ~ #canon:pasable positioned ~ ~1 ~ run function canon:diana2/zunga/techo_buscar
''')
    F('diana2/zunga/techo_poner', '''
scoreboard players set #ok dv.tmp 1
function canon:diana2/zunga/summon
playsound canon:diana.crack hostile @a[distance=..16] ~ ~2 ~ 0.8 0.7
''')
    F('diana2/zunga/cama', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #zmode dv.tmp 5
execute positioned ^1.6 ^ ^ run function canon:diana2/zunga/summon
title @s times 0 40 20
title @s subtitle {"text":"Te vi dormir.","color":"#c94a4a","italic":true}
title @s title ["",{"text":"\\ue107","font":"canon:susto","color":"white"}]
playsound canon:diana.breath hostile @s ~ ~ ~ 1 0.7
effect give @s minecraft:darkness 3 0 true
tp @s ~ ~ ~
''')
    F('diana2/llamada', '''
playsound canon:furniture.phone_ring ambient @s ^5 ^ ^-5 0.7 0.9
playsound canon:diana.name hostile @s ^-3 ^ ^-3 0.6 0.8
tellraw @s {"text":"Alguien dice tu nombre al otro lado de la pared. Con voz de alguien que conoces.","color":"#c94a4a","italic":true}
''')

    # ============================================================== DOBLES
    c.json('data/canon/loot_tables/diana2/cabeza.json', {'type': 'minecraft:generic', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:player_head',
        'functions': [{'function': 'minecraft:fill_player_head', 'entity': 'this'}]}]}]})
    headpart = ('{id:"minecraft:item_display",Tags:["dv_part","dv_dhead","dv_cal","dv_rot"],item_display:"none",view_range:1.2f,'
                'item:{id:"minecraft:player_head",Count:1b},transformation:{translation:[0f,2.0f,0f],left_rotation:[0f,0f,0f,1f],'
                'scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}')
    body = ('{id:"minecraft:item_display",Tags:["dv_part","dv_body","dv_cal","dv_rot"],item_display:"none",view_range:1.2f,'
            'item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}},transformation:{translation:[0f,1.375f,0f],'
            'left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}')
    F('diana2/doble/summon', 'summon minecraft:zombie ~ ~ ~ {Tags:["dv_brain","dv_npc2","dv_rigx","dv_new","dv_doppel","dv_horror","dv_d2rig"],'
      'Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:1b,IsBaby:0b,CanPickUpLoot:0b,'
      'ArmorItems:[{},{},{},{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}}],ArmorDropChances:[0f,0f,0f,0f],'
      'HandDropChances:[0f,0f],DeathLootTable:"canon:vacio",Passengers:[' + body + ',' + headpart + ']}\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_doppel,distance=..2,limit=1,sort=nearest] at @s run function canon:diana2/doble/init')
    F('diana2/doble/init', f'''
function canon:rig/init_common
{set_cmd('body', K['doble_idle'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.state 0
scoreboard players set @s dv.say -1
function canon:x/add_bubble
tag @s add dv_dnew2
execute as @a[tag=dv_dvictim,limit=1] at @e[type=zombie,tag=dv_dnew2,limit=1] run loot spawn ~ ~0.2 ~ loot canon:diana2/cabeza
execute on passengers if entity @s[tag=dv_dhead] run data modify entity @s item set from entity @e[type=item,distance=..4,limit=1,sort=nearest,nbt={{Item:{{id:"minecraft:player_head"}}}}] Item
execute on passengers if entity @s[tag=dv_dhead] run data modify entity @s Rotation[0] set from entity @e[type=zombie,tag=dv_dnew2,limit=1] Rotation[0]
kill @e[type=item,distance=..4,nbt={{Item:{{id:"minecraft:player_head"}}}}]
tag @s remove dv_dnew2
''')
    F('diana2/doble/intentar', '''
scoreboard players set #di_dcd dv.dev 1800
tag @s add dv_dviewer
tag @a remove dv_dvictim
tag @a[gamemode=!spectator,tag=!dv_dviewer,limit=1,sort=random] add dv_dvictim
execute unless entity @a[tag=dv_dvictim] run tag @s add dv_dvictim
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^12 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:diana2/doble/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run playsound canon:miron.estatica ambient @s ~ ~ ~ 0.5 0.7
tag @s remove dv_dviewer
tag @a remove dv_dvictim
''')
    F('diana2/doble/tick', '''
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
execute if entity @a[tag=dv_wtgt] run function canon:diana2/doble/piensa
tag @a remove dv_wtgt
''')
    F('diana2/doble/piensa', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=..13] run scoreboard players set @s dv.state 1
execute if score @s dv.state matches 1 if entity @a[tag=dv_wtgt,distance=4..] run function canon:x/walk_slow
execute if score @s dv.state matches 1 if score @s dv.say matches ..0 if score #m40 dv.clock matches 0 run function canon:diana2/doble/habla
execute if score @s dv.state matches 1 if entity @a[tag=dv_wtgt,distance=..4] run function canon:diana2/doble/descubierto
execute if score @s dv.timer matches 1200.. run function canon:diana2/zunga/se_esfuma
execute if score #m20 dv.clock matches 0 if predicate canon:azar/1en4 run tp @s ~ ~ ~ ~25 ~
''')
    pick('diana2/doble/habla', [say('???', '#9a9a9a', '#e0e0e0', t, 60, '@a[tag=dv_wtgt]') for t in [
        'Soy yo. Soy yo. Soy yo.', '¿Por qué me miras así?', 'Ven. Quiero mostrarte algo.', 'Ya no necesitas esta cara.',
        'Tú no eres tú. Yo sí.', 'Dile a Juan que lo estoy esperando.', 'Esta piel me queda mejor.']])
    F('diana2/doble/descubierto', f'''
tag @s add dv_ztwist
{set_cmd('body', K['doble_twist'])}
playsound canon:diana.scream master @a[distance=..16] ~ ~ ~ 1 1.1
execute as @a[distance=..8] at @s run function canon:x/jumpscare
tellraw @a[distance=..24] {jt('Esa persona se dobló hacia atrás y gritó con la voz de Diana.', '#c94a4a', True)}
function canon:rig/vanish
''')
    F('diana2/doble/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk,tag=!dv_dnpc] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk,tag=!dv_dnpc] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_xwalk,tag=dv_dnpc] if score #c dv.tmp matches 0..2 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk,tag=dv_dnpc] if score #c dv.tmp matches 6..8 run scoreboard players set #frame dv.tmp 2
''')
    # doble de un NPC (vagabundos de Valle Quieto y cualquier dv_humano)
    F('diana2/doble_npc/intentar', '''
scoreboard players set #di_dcd dv.dev 1200
scoreboard players set #ok dv.tmp 0
execute as @e[tag=dv_vago,tag=dv_brain,distance=..48,limit=1,sort=random] at @s run function canon:diana2/doble_npc/copiar
execute if score #ok dv.tmp matches 0 as @e[tag=dv_humano,tag=dv_brain,tag=!dv_d2rig,distance=..48,limit=1,sort=random] at @s run function canon:diana2/doble_npc/copiar
''')
    F('diana2/doble_npc/copiar', '''
scoreboard players set #ok dv.tmp 1
data remove storage canon:tmp di_item
execute on passengers if entity @s[tag=dv_body] run data modify storage canon:tmp di_item set from entity @s item
execute on passengers if entity @s[tag=dv_body] run scoreboard players operation #dicmd dv.tmp = @s dv.cmd
scoreboard players operation #pid dv.tmp = @p dv.pid
execute positioned ^2 ^ ^1 run function canon:diana2/doble_npc/summon
''')
    F('diana2/doble_npc/summon', 'summon minecraft:zombie ~ ~ ~ {Tags:["dv_brain","dv_npc2","dv_rigx","dv_new","dv_doppel","dv_dnpc","dv_horror","dv_d2rig"],'
      'Silent:1b,PersistenceRequired:1b,NoAI:1b,Invulnerable:1b,IsBaby:0b,CanPickUpLoot:0b,'
      'ArmorItems:[{},{},{},{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7319999}}],ArmorDropChances:[0f,0f,0f,0f],'
      'HandDropChances:[0f,0f],DeathLootTable:"canon:vacio",Passengers:[' + body + ']}\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_dnpc,distance=..2,limit=1,sort=nearest] at @s run function canon:diana2/doble_npc/init')
    F('diana2/doble_npc/init', '''
function canon:rig/init_common
execute on passengers if entity @s[tag=dv_body] run scoreboard players operation @s dv.cmd = #dicmd dv.tmp
execute on passengers if entity @s[tag=dv_body] run data modify entity @s item set from storage canon:tmp di_item
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.state 0
scoreboard players set @s dv.say -1
function canon:x/add_bubble
summon minecraft:interaction ~ ~ ~ {Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","dv_dnpc_click","dv_new_link"],width:0.8f,height:1.95f,response:1b}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
''')

    # ============================================================== LORE
    written_book_loot('data/canon/loot_tables/diana2/carta_juan.json', 'carta_juan', 'Carta para Juan', '#f0e4ec',
                      'Para Juan', 'Diana', [
                          'Juan:\n\nTe esperé donde dijiste. En el mismo sitio. A la misma hora. Todos los días.\n\nLa gente me mira raro. Ya no me importa.',
                          'Pedí un deseo, ¿sabes? Pedí que nadie me olvidara nunca. Para que tú no me olvidaras.\n\nAhora nadie puede. Ni aunque quiera.',
                          'Si lees esto, vuelve. No tienes que decir nada. Solo vuelve.\n\nYo ya no duermo. Si duermo, me olvidan.\n\nTuya,\nD.'],
                      ['Diana te pidió que se la des a Juan.', 'Huele a tierra mojada.'])
    written_book_loot('data/canon/loot_tables/diana2/diario.json', 'diario_diana2', 'Página del diario de Diana', '#c94a4a',
                      'Diario (página suelta)', 'D.', [
                          'Día 1.311\n\nHoy volví a ver a Santiago. Tiene los ojos de alguien que sabe algo.\n\nBana es otro. Bana me tiene miedo. Me gusta.',
                          'Aprendí a ponerme las caras de los demás. Duele un poco. Como ponerse un zapato mojado.\n\nEl perrito negro siempre me ladra. Los perros no olvidan.',
                          'Si alguien lee esto: no le mientan a Diana.\n\nNo me mientan.'],
                      ['Estaba debajo de tu almohada.'])

    # ============================================================== ADMIN
    F('admin/diana2/humana', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #dstate dv.tmp 0\nexecute positioned ^ ^ ^6 run function canon:diana2/humana/summon')
    F('admin/diana2/bana', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #dstate dv.tmp 3\nexecute positioned ^ ^ ^14 run function canon:diana2/humana/summon')
    F('admin/diana2/visita', 'tag @s add dv_di_visita\nscoreboard players set @s dv.dvis 0\ntellraw @s {"text":"[Canon Event] Visita de Diana activada para esta noche.","color":"dark_gray"}')
    F('admin/diana2/visita_ya', 'tag @s add dv_di_visita\nscoreboard players set @s dv.dvis 250\ntime set midnight')
    F('admin/diana2/borde', 'scoreboard players set #di_zcd dv.dev 0\nfunction canon:diana2/zunga/borde')
    F('admin/diana2/techo', 'scoreboard players set #di_zcd dv.dev 0\nfunction canon:diana2/zunga/techo')
    F('admin/diana2/cama', 'function canon:diana2/zunga/cama')
    F('admin/diana2/doble', 'scoreboard players set #di_dcd dv.dev 0\nfunction canon:diana2/doble/intentar')
    F('admin/diana2/doble_npc', 'scoreboard players set #di_dcd dv.dev 0\nfunction canon:diana2/doble_npc/intentar')
    for cmd, d in [('humana', 'Diana humana (pregunta por Juan)'), ('bana', 'Diana encuentra a Bana (aviso)'), ('visita', 'Visita nocturna esta noche'),
                   ('visita_ya', 'Visita nocturna ya (pone medianoche)'), ('borde', 'Zunga al borde de la vista'), ('techo', 'Zunga en el techo (en cueva)'),
                   ('cama', 'Zunga junto a la cama'), ('doble', 'Doble de un jugador'), ('doble_npc', 'Doble de un vagabundo/NPC')]:
        c.admin(f'/function canon:admin/diana2/{cmd}', d)
