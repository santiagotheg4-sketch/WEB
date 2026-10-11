execute if score #c1 dv.puzzle matches 1 as @e[type=text_display,tag=dv_clue_1] run data merge entity @s {text:'{"text":"La palanca 1\\nva ENCENDIDA","color":"#a33a4a"}'}
execute if score #c1 dv.puzzle matches 0 as @e[type=text_display,tag=dv_clue_1] run data merge entity @s {text:'{"text":"La palanca 1\\nva APAGADA","color":"#a33a4a"}'}
execute if score #c2 dv.puzzle matches 1 as @e[type=text_display,tag=dv_clue_2] run data merge entity @s {text:'{"text":"La palanca 2\\nva ENCENDIDA","color":"#a33a4a"}'}
execute if score #c2 dv.puzzle matches 0 as @e[type=text_display,tag=dv_clue_2] run data merge entity @s {text:'{"text":"La palanca 2\\nva APAGADA","color":"#a33a4a"}'}
execute if score #c3 dv.puzzle matches 1 as @e[type=text_display,tag=dv_clue_3] run data merge entity @s {text:'{"text":"La palanca 3\\nva ENCENDIDA","color":"#a33a4a"}'}
execute if score #c3 dv.puzzle matches 0 as @e[type=text_display,tag=dv_clue_3] run data merge entity @s {text:'{"text":"La palanca 3\\nva APAGADA","color":"#a33a4a"}'}
execute if score #c4 dv.puzzle matches 1 as @e[type=text_display,tag=dv_clue_4] run data merge entity @s {text:'{"text":"La palanca 4\\nva ENCENDIDA","color":"#a33a4a"}'}
execute if score #c4 dv.puzzle matches 0 as @e[type=text_display,tag=dv_clue_4] run data merge entity @s {text:'{"text":"La palanca 4\\nva APAGADA","color":"#a33a4a"}'}
scoreboard players set #clues dv.puzzle 1
