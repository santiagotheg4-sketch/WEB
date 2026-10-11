function canon:diana/jumpscare
damage @s 4 canon:diana
effect give @s minecraft:nausea 10 0 true
effect give @s minecraft:weakness 60 0 true
function canon:diana/par/release
scoreboard players remove @s dv.dia 350
scoreboard players set @s[scores={dv.dia=..-1}] dv.dia 0
scoreboard players set @s dv.dcd 120
tellraw @s {"text":"Despiertas de golpe. No estabas soñando.","color":"dark_red","italic":true}
