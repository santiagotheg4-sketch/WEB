execute if score #cata_built dv.build matches 2 run function canon:kevin/cata/enter
execute unless score #cata_built dv.build matches 2 if score #kev dv.dev matches 3 run schedule function canon:kevin/cata/enter_wait 20t replace
