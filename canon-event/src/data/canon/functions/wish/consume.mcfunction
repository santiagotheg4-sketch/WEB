execute store result score #has dv.tmp run clear @s minecraft:carrot_on_a_stick{canon:{id:"hueso_deseo"}} 0
execute if score #has dv.tmp matches 0 run tellraw @s {"text":"El hueso ya no está en tus manos.","color":"gray","italic":true}
execute if score #has dv.tmp matches 1.. run function canon:wish/grant
