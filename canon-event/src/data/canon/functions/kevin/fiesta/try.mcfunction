execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_dia] run function canon:kevin/fiesta/day_no
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_noche] run function canon:kevin/fiesta/start
