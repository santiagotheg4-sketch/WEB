execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound canon:juli.chime ambient @a[distance=..12] ~ ~ ~ 0.4 1.3
execute if score @s dv.state matches 4 run function canon:juli/click/dream
execute if score @s dv.state matches 1 run function canon:juli/click/others
execute if score @s dv.state matches 1 unless entity @s[tag=dv_jgave] run function canon:juli/gift
execute if score @s dv.state matches 2 if entity @a[tag=dv_talker,tag=dv_santi] run function canon:juli/start_scene
execute if score @s dv.state matches 2 unless entity @a[tag=dv_talker,tag=dv_santi] run function canon:juli/click/others
