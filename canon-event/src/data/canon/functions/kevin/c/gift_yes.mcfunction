scoreboard players set #k dv.tmp 0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en5 run function canon:kevin/c/gift_yes/o0
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en4 run function canon:kevin/c/gift_yes/o1
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en3 run function canon:kevin/c/gift_yes/o2
execute if score #k dv.tmp matches 0 if predicate canon:azar/1en2 run function canon:kevin/c/gift_yes/o3
execute if score #k dv.tmp matches 0 run function canon:kevin/c/gift_yes/o4
scoreboard players set @a[tag=dv_ktalk] dv.kpcd 1200
