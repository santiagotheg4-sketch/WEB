tag @s remove dv_ringing
stopsound @a[distance=..32] block canon:furniture.phone_ring
playsound canon:items.radio_voice block @a[tag=dv_talker] ~ ~ ~ 1 0.8
execute if entity @a[tag=dv_talker,scores={dv.obs=1..}] run tellraw @a[tag=dv_talker] [{"text":"Teléfono: ","color":"#d77a8a"},{"text":"¿Por qué no me contestabas? Te estoy viendo. Qué bonita/o te ves con esa ropa.","color":"white","italic":true}]
execute unless entity @a[tag=dv_talker,scores={dv.obs=1..}] run tellraw @a[tag=dv_talker] [{"text":"Teléfono: ","color":"gray"},{"text":"...respira... respira... *clic*","color":"white","italic":true}]
