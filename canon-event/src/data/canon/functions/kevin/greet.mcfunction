playsound canon:kevin.hey neutral @a[distance=..24] ~ ~1.6 ~ 1 1
execute if score #kprog dv.dev matches 0 run function canon:kevin/first
execute unless score #kprog dv.dev matches 0 run function canon:kevin/greet_any
