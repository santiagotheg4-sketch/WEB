tag @s remove dv_waving
tag @s remove dv_fastwave
tag @s remove dv_offering
tag @s remove dv_covering
tag @s remove dv_openarms
execute if entity @s[tag=dv_sitting] run function canon:devota/pose/req_normal
tag @s remove dv_sitting
