execute if score @s dv.timer matches ..150 if score #m4 dv.clock matches 0 run function canon:juli/face
execute if score @s dv.timer matches 20 run function canon:juli/ask/hello
execute if score @s dv.timer matches 90 run function canon:juli/ask/more
execute if score @s dv.timer matches 165 run function canon:juli/ask/end
execute if score @s dv.timer matches 230.. run function canon:juli/start_bye
execute unless entity @a[tag=dv_jtgt,distance=..40] run function canon:juli/vanish
