scoreboard players operation #id dv.tmp = @s dv.id
scoreboard players set #rider dv.tmp 0
execute store success score #rider dv.tmp on passengers if entity @s[type=player]
execute if score #rider dv.tmp matches 1 run function canon:car/driving
execute if score #rider dv.tmp matches 0 run function canon:car/parked
execute unless data entity @s SaddleItem run data merge entity @s {SaddleItem:{id:"minecraft:saddle",Count:1b}}
