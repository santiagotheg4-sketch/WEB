scoreboard players set @s dv.joined 1
scoreboard players set @s dv.hud 1
scoreboard players set @s dv.obs 0
execute if score #kit dv.cfg matches 1 run function canon:player/kit
tellraw @s ["",{"text":"\n☾ CANON EVENT ☽\n","color":"#d77a8a","bold":true},{"text":"Alguien dejó un sobre en tu bolsillo. Dentro hay un diario y un boleto de autobús a un pueblo que no aparece en los mapas.\n","color":"gray","italic":true},{"text":"[Abrir menú]","color":"#e8c9a8","clickEvent":{"action":"run_command","value":"/trigger dv.menu set 1"},"hoverEvent":{"action":"show_text","contents":"Cómo jugar, ajustes y comandos"}}]
