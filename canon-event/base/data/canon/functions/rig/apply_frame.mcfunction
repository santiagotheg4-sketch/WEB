scoreboard players operation @s dv.frame = #frame dv.tmp
execute on passengers if entity @s[tag=dv_body,tag=dv_ready] run function canon:rig/set_body_cmd
