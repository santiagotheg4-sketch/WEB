execute unless score #kev dv.dev matches 1 run tellraw @s {"text":"Ya no hay nada que tomar.","color":"gray","italic":true}
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 21 unless entity @s[tag=dv_kdrug] run function canon:kevin/fiesta/drink
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 22 run function canon:kevin/fiesta/refuse
