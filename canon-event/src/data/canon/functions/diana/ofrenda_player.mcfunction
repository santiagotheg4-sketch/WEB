scoreboard players remove @s dv.dia 300
scoreboard players set @s[scores={dv.dia=..-1}] dv.dia 0
scoreboard players set @s dv.dcd 300
scoreboard players operation #pid dv.tmp = @s dv.pid
execute as @e[type=zombie,tag=dv_diana] if score @s dv.target = #pid dv.tmp at @s run function canon:diana/vanish_quiet
tellraw @s {"text":"Las velas se apagan solas. Diana aceptó lo que era suyo. Por esta noche.","color":"#b3261e","italic":true}
