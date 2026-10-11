from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json

def models_nicolas():
    at = Atlas('nicolas', 21)
    skin = '#e3cbbb'

    def shirt_paint(a, f, r):
        if f == 'north':
            x, y, w, h = r
            # calavera gris pequeña (estampado emo)
            cx, cy = x + w // 2 - 3, y + 4
            rect(a, cx, cy, 6, 5, '#6d6d72'); px(a, cx + 1, cy + 2, '#121214'); px(a, cx + 4, cy + 2, '#121214')
            rect(a, cx + 1, cy + 5, 4, 1, '#6d6d72')

    def arm_paint(a, f, r):
        x, y, w, h = r
        rect(a, x, y + h - 4, w, 4, skin)
        # muñequeras con taches
        rect(a, x, y + h - 6, w, 2, '#0b0b0b')
        for i in range(0, w, 2):
            px(a, x + i, y + h - 6, '#b9b9c0')

    c = dict(skin=skin, pants='#0f0f12', shoes='#141414', belt='#2a2a2e', shirt='#141417', sleeve='#141417',
             shirt_paint=shirt_paint, arm_paint=arm_paint)
    P = humanoid_parts(at, c, 'chubby')
    for n in ['idle', 'walk_a', 'walk_b', 'reach']:
        write_model('nicolas_' + n, 'nicolas', pose(P, n))
    at.save()
    ah = Atlas('nicolas_cabeza', 22)
    hair = '#0a0a0c'
    H = head_parts(ah, dict(skin=skin, hair=hair), 'emo')
    base = dict(iris='#1a1a1a', brow='#050505', lips='#6a3a44', emo_fringe=False, hair=hair)
    exprs = {
        'burla': dict(base, mouth='grin', eyes='normal'),
        'odio': dict(base, mouth='frown', eyes='angry'),
        'grito': dict(base, mouth='scream', eyes='void'),
    }
    for n, st in exprs.items():
        r = face_rect(ah)
        fe = face_element(ah, r, skin, st, 'face_' + n)
        # sombra de delineador
        write_model('nicolas_cabeza_' + n, 'nicolas_cabeza', all_elements(H) + [fe])
    ah.save()






INSULTOS = [
    'Nadie te va a extrañar aquí abajo.',
    'Cava, cava... estás cavando tu propia tumba.',
    '¿Crees que eres especial? Eres un chiste.',
    'Todos se ríen de ti cuando no estás.',
    'Mírate. Das pena.',
    'Aquí abajo nadie oye tus gritos.',
    'Eres lento. Eres débil. Eres mío.',
    'Tus amigos ya se fueron sin ti.',
    'Hueles a miedo.',
    'No eres nadie. Nunca lo fuiste.',
    '¿Por qué sigues intentando? Ya perdiste.',
    'Corre, gordito... ah no, ese soy yo. Jajaja.',
]


def gen_nicolas():
    K = CMD
    F('nicolas/try', '''
scoreboard players set @s dv.ncd 420
execute if entity @e[type=zombie,tag=dv_nicolas,distance=..96] run scoreboard players set @s dv.ncd 60
execute unless entity @e[type=zombie,tag=dv_nicolas,distance=..96] run function canon:nicolas/try2
''')
    F('nicolas/try2', f'''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-8 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:nicolas/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run tellraw @s {jt('Pasos pesados detrás de ti. Alguien se ríe bajito.', '#8a8a96', True)}
execute if score #ok dv.tmp matches 1 run playsound canon:nicolas.risa hostile @s ^ ^ ^-10 1 0.9
execute if score #ok dv.tmp matches 1 run playsound canon:mina.ambient ambient @s ~ ~ ~ 0.8 1
execute if score #ok dv.tmp matches 1 as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/n/nicolas
''')
    F('nicolas/summon', rig_summon(['dv_nicolas'], 'Nicolás', '#8a8a96', health=40, invul=False) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_nicolas,distance=..2,limit=1,sort=nearest] at @s run function canon:nicolas/init')
    F('nicolas/init', f'''
function canon:rig/init_common
{set_cmd('body', K['nicolas_idle'])}
{head(K['nicolas_cabeza_burla'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer2 60
function canon:x/add_bubble
''')
    F('nicolas/tick', '''
function canon:x/links_follow
tag @s remove dv_xwalk
tag @s remove dv_nreach
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
scoreboard players operation #tgt dv.tmp = @s dv.target
tag @a remove dv_wtgt
execute as @a[distance=..48,gamemode=!spectator] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
scoreboard players add @s dv.timer 1
scoreboard players set #ngo dv.tmp 0
execute unless entity @a[tag=dv_wtgt] run scoreboard players set #ngo dv.tmp 1
execute if entity @a[tag=dv_wtgt,y=56,dy=400] run scoreboard players set #ngo dv.tmp 1
execute if score @s dv.timer matches 1400.. run scoreboard players set #ngo dv.tmp 1
execute if score #ngo dv.tmp matches 0 run function canon:nicolas/hunt
execute if score #ngo dv.tmp matches 1 run function canon:nicolas/leave
tag @a remove dv_wtgt
''')
    F('nicolas/hunt', f'''
execute if entity @a[tag=dv_wtgt,distance=1.5..] run function canon:nicolas/step
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #90 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:nicolas.pasos hostile @a[distance=..24] ~ ~ ~ 1 0.9
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #140 dv.math
execute if score #c dv.tmp matches 20 run function canon:nicolas/insult
scoreboard players remove @s[scores={{dv.timer2=1..}}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..3] run tag @s add dv_nreach
execute if entity @a[tag=dv_wtgt,distance=..1.6] unless score @s dv.timer2 matches 1.. run function canon:nicolas/hit
''')
    F('nicolas/step', '''
tag @s add dv_xwalk
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.15 run tp @s ~ ~ ~ ~ ~
execute at @s run function canon:diana/ground
''')
    opts = []
    for i, t in enumerate(INSULTOS):
        h = K['nicolas_cabeza_odio'] if i % 2 else K['nicolas_cabeza_burla']
        opts.append(bubble('dv_xbubble', t, '#b9b9c6', 80) + '\n' + chat('Nicolás', '#8a8a96', t, '@a[tag=dv_wtgt]') + '\n' + head(h))
    pick('nicolas/insult', opts)
    F('nicolas/hit', f'''
scoreboard players set @s dv.timer2 24
damage @a[tag=dv_wtgt,limit=1] 3 minecraft:mob_attack by @s
playsound canon:nicolas.risa hostile @a[distance=..16] ~ ~ ~ 1 1.1
{head(K['nicolas_cabeza_grito'])}
''')
    F('nicolas/leave', '''
playsound canon:nicolas.risa hostile @a[distance=..24] ~ ~ ~ 0.8 0.8
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.7 0.3 0.01 20 normal
function canon:rig/despawn
''')
    F('nicolas/died', f'''
playsound canon:nicolas.risa hostile @a[distance=..24] ~ ~ ~ 1 0.6
tellraw @a[distance=..24] {jt('Nicolás se deshace en humo negro. Su risa sigue sonando en la piedra.', '#8a8a96', True)}
''')
    # susto al picar piedra
    F('nicolas/mined', '''
scoreboard players set @s dv.mst 0
scoreboard players set @s dv.mds 0
execute if score #nicolas dv.cfg matches 1 if predicate canon:en_superficie if entity @s[y=-64,dy=114] unless score @s dv.ncd matches 61.. if predicate canon:azar/1en150 run function canon:nicolas/face_scare
''')
    F('nicolas/face_scare', f'''
scoreboard players set @s dv.ncd 900
execute anchored eyes positioned ^ ^ ^2.4 run summon minecraft:item_display ~ ~ ~ {{Tags:["dv_nface","dv_nface_new"],item_display:"none",brightness:{{sky:15,block:12}},view_range:0.6f,item:{{id:"minecraft:leather_horse_armor",Count:1b,tag:{{CustomModelData:{K['nicolas_cabeza_grito']}}}}},transformation:{{translation:[0f,-0.12f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,0f,0f,1f]}}}}
tag @s add dv_nface_me
execute as @e[type=item_display,tag=dv_nface_new] at @s facing entity @a[tag=dv_nface_me,limit=1] eyes run tp @s ~ ~ ~ ~ 0
tag @s remove dv_nface_me
execute if score #flip dv.cfg matches 1 as @e[type=item_display,tag=dv_nface_new] run data modify entity @s transformation.right_rotation set value [0f,1f,0f,0f]
execute as @e[type=item_display,tag=dv_nface_new] run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[2.4f,2.4f,2.4f],translation:[0f,-0.5f,0f]}}}}
tag @e[type=item_display,tag=dv_nface_new] remove dv_nface_new
playsound canon:nicolas.maldito master @s ~ ~ ~ 1 0.95
playsound canon:fx.stinger master @s ~ ~ ~ 0.9 1
effect give @s minecraft:darkness 3 0 true
title @s times 0 25 10
title @s subtitle {{"text":"¡MALDITO!","color":"#b01212","bold":true}}
title @s title {{"text":" "}}
function canon:fx/shake_big
''')
    F('nicolas/face_tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 22 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{scale:[0f,0f,0f]}}
execute if score @s dv.timer matches 22 run particle minecraft:large_smoke ~ ~ ~ 0.4 0.4 0.4 0.02 20 normal
execute if score @s dv.timer matches 32.. run kill @s
''')


# =================================================================== MIRÓN


def gen_luna():
    F('luna/n/nicolas', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_luna_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¡Ese chico de negro huele a rabia! ¡Grrr! ¡Corre!","color":"#ffd27a"}',background:1342177280}
scoreboard players set @s dv.say 60
function canon:luna/bark2
scoreboard players set @s dv.talkcd 600
''')


# =================================================================== PARCHES a archivos existentes


NICOLAS_MODELS = (['nicolas_' + n for n in ['idle', 'walk_a', 'walk_b', 'reach']]
                  + ['nicolas_cabeza_' + n for n in ['burla', 'odio', 'grito']])


def build(c):
    shim.use(c)
    shim.models(NICOLAS_MODELS, 7320126)
    from canon import skins as SK
    SK.build_character('nicolas', dict(skin='#e3cbbb', hair='#0a0a0c', hair_style='emo', eyes='#1a1a1a', top='#141417', top_style='tshirt',
                                       print='#6d6d72', pants='#0f0f12', shoes='#141414', lips='#6a3a44', extras=['makeup', 'earrings', 'belt']), c.out,
                       ('idle', 'walk_a', 'walk_b', 'reach'), [('burla', 'smile'), ('odio', 'angry'), ('grito', 'void')])
    c.objective('dv.mst', 'minecraft.mined:minecraft.stone')
    c.objective('dv.mds', 'minecraft.mined:minecraft.deepslate')
    c.objective('dv.ncd')
    for n in (4, 90, 140):
        c.const(n)
    c.on('player', '''
execute if score @s dv.mst matches 1.. run function canon:nicolas/mined
execute if score @s dv.mds matches 1.. run function canon:nicolas/mined
''')
    c.on('second', '''
scoreboard players remove @a[scores={dv.ncd=1..}] dv.ncd 1
execute if score #nicolas dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @s[y=-64,dy=104] if score @s dv.ncd matches ..0 if predicate canon:azar/1en300 run function canon:nicolas/try
execute unless score #nicolas dv.cfg matches 1 as @e[type=zombie,tag=dv_nicolas] at @s run function canon:rig/despawn
''')
    c.on('tick', 'execute as @e[type=item_display,tag=dv_nface] at @s run function canon:nicolas/face_tick')
    c.npc('dv_nicolas', 'nicolas/tick')
    c.frames('dv_nicolas', 'nicolas/frames')
    c.die('dv_nicolas', 'nicolas/died')
    c.on('luna_notice', 'execute if score @s dv.talkcd matches ..0 if entity @e[type=zombie,tag=dv_nicolas,distance=..16] run function canon:luna/n/nicolas')
    F('nicolas/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_nreach] run scoreboard players set #frame dv.tmp 3
''')
    gen_nicolas()
    gen_luna()
    c.admin('/function canon:admin/spawn/nicolas', 'Traer a Nicolás')
    c.admin('/function canon:admin/susto_mina', 'Probar el susto de la mina')
    F('admin/spawn/nicolas', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^6 run function canon:nicolas/summon')
    F('admin/susto_mina', 'function canon:nicolas/face_scare')
