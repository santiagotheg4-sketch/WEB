scoreboard players set @s dv.cool 14
execute store result score #ammo dv.tmp run clear @s minecraft:iron_nugget{canon:{id:"balas"}} 0
execute if score #ammo dv.tmp matches 0 run playsound canon:items.revolver_click player @a[distance=..16] ~ ~ ~ 1 1
execute if score #ammo dv.tmp matches 0 run title @s actionbar {"text":"Sin balas.","color":"gray"}
execute if score #ammo dv.tmp matches 1.. run function canon:items/revolver/fire
