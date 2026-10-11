function canon:curse/end_by_escape
title @s times 20 100 40
title @s subtitle {"text":"El amor se quedó en Valle Quieto. Por ahora.","color":"gray","italic":true}
title @s title {"text":"ESCAPASTE","color":"#9fd8b0","bold":true}
playsound canon:fx.music_box_end master @s ~ ~ ~ 1 1
playsound canon:car.horn master @s ~ ~ ~ 1 1
give @s minecraft:carrot_on_a_stick{CustomModelData:7310017,canon:{id:"llaves"},display:{Name:'{"text":"Llaves del descapotable","italic":false,"color":"#c9ced6"}',Lore:['{"text":"Pieza para el descapotable.","italic":false,"color":"gray"}','{"text":"Fuera del pueblo: clic derecho para","italic":false,"color":"gray"}','{"text":"traer tu carro.","italic":false,"color":"gray"}']},Unbreakable:1b} 1
