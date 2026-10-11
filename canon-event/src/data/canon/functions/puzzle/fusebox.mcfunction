execute if score #sol3 dv.puzzle matches 1 run tellraw @a[tag=dv_talker] {"text":"La caja de fusibles zumba. Ya hay corriente.","color":"gray","italic":true}
execute if score #sol3 dv.puzzle matches 0 if entity @a[tag=dv_talker,nbt={SelectedItem:{tag:{canon:{id:"fusible"}}}}] run function canon:puzzle/fusebox_ok
execute if score #sol3 dv.puzzle matches 0 unless entity @a[tag=dv_talker,nbt={SelectedItem:{tag:{canon:{id:"fusible"}}}}] run tellraw @a[tag=dv_talker] {"text":"La caja de fusibles está vacía. Hace falta un fusible (en la mano).","color":"gray","italic":true}
