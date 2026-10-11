title @a[predicate=canon:visitable] times 5 70 25
title @a[predicate=canon:visitable] subtitle {"text":"Corre.","color":"#c43a4a","italic":true}
title @a[predicate=canon:visitable] title {"text":"ELLA SE ROMPIÓ","color":"#c43a4a","bold":true}
execute as @a[predicate=canon:visitable] at @s run playsound canon:devota.scream master @s ~ ~ ~ 0.8 0.8
execute as @a[predicate=canon:visitable] run function canon:fx/shake_big
