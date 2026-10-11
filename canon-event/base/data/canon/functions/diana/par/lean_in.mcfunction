tag @s add dv_dme2
execute as @a[tag=dv_dtgt,limit=1] at @s rotated ~ 0 positioned ^ ^ ^1.35 run tp @e[type=zombie,tag=dv_dme2,limit=1] ~ ~ ~
tag @s remove dv_dme2
execute at @s run function canon:diana/face
function canon:diana/pose/req_stretch
