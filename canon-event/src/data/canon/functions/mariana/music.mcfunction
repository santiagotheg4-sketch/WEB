scoreboard players set @s dv.music 331
execute if score @s dv.talk matches 0 run playsound canon:music.mariana_baile record @a[distance=..28] ~ ~ ~ 0.5 1
execute if score @s dv.talk matches 1..2 run playsound canon:music.mariana_baile record @a[distance=..28] ~ ~ ~ 0.7 1.06
execute if score @s dv.talk matches 3..4 run playsound canon:music.mariana_baile record @a[distance=..28] ~ ~ ~ 0.8 1.15
execute if score @s dv.talk matches 5.. run playsound canon:music.mariana_baile record @a[distance=..28] ~ ~ ~ 0.9 1.3
