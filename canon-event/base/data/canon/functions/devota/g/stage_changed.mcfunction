execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 4 run function canon:devota/g/notice_4
execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 5 run function canon:devota/g/notice_5
execute if score #stage dv.dev > #oldstage dv.dev if score #stage dv.dev matches 6 run function canon:devota/g/notice_6
execute if score #stage dv.dev < #oldstage dv.dev if score #stage dv.dev matches 1..3 run title @a[predicate=canon:visitable] actionbar {"text":"Ella parece más tranquila.","color":"#d77a8a","italic":true}
execute as @e[type=zombie,tag=dv_devota] at @s if score #stage dv.dev matches 5.. run function canon:devota/turn_dangerous
execute as @e[type=zombie,tag=dv_devota] at @s if score #stage dv.dev < #oldstage dv.dev if score #stage dv.dev matches ..4 unless score #townmode dv.dev matches 1 run function canon:devota/start_leave
function canon:luna/react/devota_stage
