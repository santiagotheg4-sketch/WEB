execute on passengers if entity @s[tag=dv_head] run scoreboard players set @s dv.cmd 7320124
execute on passengers if entity @s[tag=dv_head,tag=dv_ready] run data modify entity @s item.tag.CustomModelData set value 7320124
playsound canon:miron.grito master @a[distance=..12] ~ ~ ~ 1 0.8
execute as @a[distance=..12] at @s run function canon:x/jumpscare
tellraw @a[distance=..12] {"text": "Eso no era Kevin.", "color": "#c94a4a", "italic": true}
function canon:rig/vanish
