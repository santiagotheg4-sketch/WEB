scoreboard players add @s dv.travel 1
execute if score @s dv.travel matches 120 run title @s subtitle {"text":"Las luces de un pueblo aparecen a lo lejos.","color":"gray","italic":true}
execute if score @s dv.travel matches 120 run title @s title {"text":" "}
execute if score @s dv.travel matches 120.. if score #built dv.build matches 1 if score #m40 dv.clock matches 0 run title @s actionbar {"text":"El pueblo se está despertando... (construyendo Valle Quieto)","color":"dark_gray"}
execute if score @s dv.travel matches 160.. if score #built dv.build matches 2 run function canon:travel/arrive
