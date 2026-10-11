execute if entity @a[tag=dv_talker,nbt={SelectedItem:{tag:{canon:{id:"billete"}}}}] run function canon:furn/vend
execute unless entity @a[tag=dv_talker,nbt={SelectedItem:{tag:{canon:{id:"billete"}}}}] run tellraw @a[tag=dv_talker] {"text":"La máquina pide un billete (tenlo en la mano).","color":"gray","italic":true}
