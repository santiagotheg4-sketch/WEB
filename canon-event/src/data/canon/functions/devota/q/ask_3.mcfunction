scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=text_display,tag=dv_dev_bubble] if score @s dv.id = #id dv.tmp run data merge entity @s {text:'{"text":"¿Soy tu favorita?","color":"#d77a8a"}',background:1342177280}
scoreboard players set @s dv.say 300
playsound canon:ui.blip neutral @a[distance=..16] ~ ~1.6 ~ 0.5 1.25
scoreboard players set #q dv.dev 3
scoreboard players set #qgood dv.dev 1
scoreboard players set #qt dv.dev 15
scoreboard players enable @a[distance=..24] dv.resp
scoreboard players set @a[distance=..24] dv.resp 0
tellraw @a[distance=..24] ["",{"text":"\n","color":"white"},{"text":"La Devota: ","color":"#d77a8a"},{"text":"¿Soy tu favorita?\n","color":"white","italic":true},{"text":"   [Sí]","color":"#9fd8b0","bold":true,"clickEvent":{"action":"run_command","value":"/trigger dv.resp set 1"}},{"text":"   [No]","color":"#e84a4a","bold":true,"clickEvent":{"action":"run_command","value":"/trigger dv.resp set 2"}}]
