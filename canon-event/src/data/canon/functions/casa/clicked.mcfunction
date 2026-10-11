execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound canon:juli.chime ambient @a[distance=..12] ~ ~ ~ 0.4 1.3
scoreboard players set @s dv.timer2 0
tellraw @a[tag=dv_talker] ["",{"text": "\nJULI\n", "color": "#f2a7c3"},{"text": " [¿Dónde estamos?] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 1"}},{"text": " [¿Qué haces?] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 2"}},{"text": " [¿Estás bien?] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 3"}},{"text": " [Me tengo que ir] ", "color": "#e8c9a8", "clickEvent": {"action": "run_command", "value": "/trigger dv.jr set 4"}}]
