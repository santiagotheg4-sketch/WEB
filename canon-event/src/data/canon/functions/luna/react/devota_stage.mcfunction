execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 4 run execute as @e[type=wolf,tag=dv_luna,limit=1] at @s run function canon:luna/r/st4
execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 5 run execute as @e[type=wolf,tag=dv_luna,limit=1] at @s run function canon:luna/r/st5
execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 6 run execute as @e[type=wolf,tag=dv_luna,limit=1] at @s run function canon:luna/r/st6
execute if score #stage dv.dev < #oldstage dv.dev run execute as @e[type=wolf,tag=dv_luna,limit=1] at @s run function canon:luna/r/better
