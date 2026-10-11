execute as @e[type=item_display,tag=dv_nface] at @s run function canon:nicolas/face_tick
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/tick
execute if score #casa_built dv.build matches 1 run function canon:casa/build_try
execute if score #cata_built dv.build matches 1 run function canon:kevin/cata/build_try
