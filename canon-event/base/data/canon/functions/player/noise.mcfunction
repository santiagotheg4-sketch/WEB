scoreboard players set @s dv.noise 0
execute if score @s dv.crouch matches 1.. run scoreboard players set @s dv.noise 1
execute if score @s dv.walk matches 1.. run scoreboard players set @s dv.noise 2
execute if score @s dv.swim matches 1.. run scoreboard players set @s dv.noise 2
execute if score @s dv.jump matches 1.. run scoreboard players set @s dv.noise 3
execute if score @s dv.sprint matches 1.. run scoreboard players set @s dv.noise 3
execute if score @s dv.horse matches 1.. run scoreboard players set @s dv.noise 4
execute if score @s dv.noisecd matches 1.. run scoreboard players set @s dv.noise 5
scoreboard players remove @s[scores={dv.noisecd=1..}] dv.noisecd 1
execute if score @s dv.sleep matches 1.. run scoreboard players set @s dv.noise 0
scoreboard players set @s dv.walk 0
scoreboard players set @s dv.sprint 0
scoreboard players set @s dv.crouch 0
scoreboard players set @s dv.jump 0
scoreboard players set @s dv.horse 0
scoreboard players set @s dv.swim 0
