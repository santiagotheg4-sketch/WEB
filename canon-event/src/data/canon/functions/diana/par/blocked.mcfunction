scoreboard players set #go dv.tmp 0
clear @s minecraft:paper{canon:{id:"atrapasuenos"}} 1
scoreboard players set @s dv.parcd 12000
playsound minecraft:block.wool.break player @s ~ ~ ~ 1 0.7
tellraw @s {"text":"Entre sueños sientes que alguien se acerca a tu cama... y se aleja. El atrapasueños se rompió.","color":"#9ab8f0","italic":true}
