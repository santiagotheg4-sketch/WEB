# Devoción — inicialización
scoreboard objectives add dv.tmp dummy
scoreboard objectives add dv.math dummy
scoreboard objectives add dv.cfg dummy
scoreboard objectives add dv.clock dummy
scoreboard objectives add dv.pid dummy
scoreboard objectives add dv.id dummy
scoreboard objectives add dv.walk minecraft.custom:minecraft.walk_one_cm
scoreboard objectives add dv.sprint minecraft.custom:minecraft.sprint_one_cm
scoreboard objectives add dv.crouch minecraft.custom:minecraft.crouch_one_cm
scoreboard objectives add dv.jump minecraft.custom:minecraft.jump
scoreboard objectives add dv.horse minecraft.custom:minecraft.horse_one_cm
scoreboard objectives add dv.swim minecraft.custom:minecraft.swim_one_cm
scoreboard objectives add dv.noise dummy
scoreboard objectives add dv.noisecd dummy
scoreboard objectives add dv.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add dv.cool dummy
scoreboard objectives add dv.deseo trigger
scoreboard objectives add dv.menu trigger
scoreboard objectives add dv.wish dummy
scoreboard objectives add dv.obs dummy
scoreboard objectives add dv.state dummy
scoreboard objectives add dv.timer dummy
scoreboard objectives add dv.timer2 dummy
scoreboard objectives add dv.watch dummy
scoreboard objectives add dv.lose dummy
scoreboard objectives add dv.jeal dummy
scoreboard objectives add dv.anim dummy
scoreboard objectives add dv.frame dummy
scoreboard objectives add dv.cmd dummy
scoreboard objectives add dv.flash dummy
scoreboard objectives add dv.calib dummy
scoreboard objectives add dv.talk dummy
scoreboard objectives add dv.talkdec dummy
scoreboard objectives add dv.death deathCount
scoreboard objectives add dv.leave minecraft.custom:minecraft.leave_game
scoreboard objectives add dv.hp dummy
scoreboard objectives add dv.hpold dummy
scoreboard objectives add dv.target dummy
scoreboard objectives add dv.seen dummy
scoreboard objectives add dv.town dummy
scoreboard objectives add dv.gm dummy
scoreboard objectives add dv.rx dummy
scoreboard objectives add dv.ry dummy
scoreboard objectives add dv.rz dummy
scoreboard objectives add dv.rdim dummy
scoreboard objectives add dv.travel dummy
scoreboard objectives add dv.respawn dummy
scoreboard objectives add dv.vanish dummy
scoreboard objectives add dv.inv dummy
scoreboard objectives add dv.sleep dummy
scoreboard objectives add dv.pill dummy
scoreboard objectives add dv.rain dummy
scoreboard objectives add dv.build dummy
scoreboard objectives add dv.parts dummy
scoreboard objectives add dv.joined dummy
scoreboard objectives add dv.hud dummy
scoreboard objectives add dv.puzzle dummy
scoreboard objectives add dv.seq dummy
scoreboard objectives add dv.debug dummy
scoreboard objectives add dv.ev dummy
scoreboard objectives add dv.say dummy
scoreboard objectives add dv.music dummy
scoreboard objectives add dv.on dummy
scoreboard objectives add dv.car dummy
scoreboard objectives add dv.gift dummy
scoreboard objectives add dv.dia dummy
scoreboard objectives add dv.dcd dummy
scoreboard objectives add dv.dhunt dummy
scoreboard objectives add dv.par dummy
scoreboard objectives add dv.parcd dummy
scoreboard objectives add dv.bed minecraft.custom:minecraft.sleep_in_bed
scoreboard objectives add dv.zz dummy
scoreboard objectives add dv.bat dummy
scoreboard objectives add dv.lint dummy
scoreboard objectives add dv.posereq dummy
scoreboard objectives add dv.posecur dummy
scoreboard objectives add dv.dleft dummy
scoreboard objectives add dv.yaw dummy
scoreboard objectives add dv.juli dummy
scoreboard objectives add dv.jcd dummy
scoreboard objectives add dv.sueno dummy
scoreboard objectives add dv.sfase dummy
scoreboard objectives add dv.jline dummy
scoreboard objectives add dv.escena dummy
scoreboard objectives add dv.dev dummy
scoreboard objectives add dv.resp trigger
scoreboard objectives add dv.mode dummy
scoreboard objectives add dv.pmode dummy
scoreboard objectives add dv.idle dummy
scoreboard objectives add dv.talkcd dummy
scoreboard objectives add dv.near dummy
scoreboard objectives add dv.shake dummy
scoreboard objectives add dv.hudon dummy
scoreboard objectives add dv.lnear dummy
scoreboard players set #-1 dv.math -1
scoreboard players set #2 dv.math 2
scoreboard players set #3 dv.math 3
scoreboard players set #4 dv.math 4
scoreboard players set #5 dv.math 5
scoreboard players set #8 dv.math 8
scoreboard players set #10 dv.math 10
scoreboard players set #12 dv.math 12
scoreboard players set #16 dv.math 16
scoreboard players set #20 dv.math 20
scoreboard players set #24 dv.math 24
scoreboard players set #40 dv.math 40
scoreboard players set #60 dv.math 60
scoreboard players set #90 dv.math 90
scoreboard players set #100 dv.math 100
scoreboard players set #200 dv.math 200
scoreboard players set #225 dv.math 225
scoreboard players set #360 dv.math 360
scoreboard players set #1000 dv.math 1000
execute unless score #init dv.cfg matches 1 run function canon:config/defaults
execute unless score #next dv.id matches 1.. run scoreboard players set #next dv.id 1
execute unless score #nextpid dv.pid matches 1.. run scoreboard players set #nextpid dv.pid 1
execute unless score #built dv.build matches 0.. run scoreboard players set #built dv.build 0
execute unless score #parts dv.parts matches 0.. run scoreboard players set #parts dv.parts 0
execute unless score #sueno_built dv.build matches 0.. run scoreboard players set #sueno_built dv.build 0
execute unless score #diana dv.cfg matches 0.. run scoreboard players set #diana dv.cfg 1
execute unless score #paralisis dv.cfg matches 0.. run scoreboard players set #paralisis dv.cfg 1
execute unless score #senales dv.cfg matches 0.. run scoreboard players set #senales dv.cfg 1
execute unless score #juli dv.cfg matches 0.. run scoreboard players set #juli dv.cfg 1
execute unless score #devota dv.cfg matches 0.. run scoreboard players set #devota dv.cfg 1
execute unless score #luna dv.cfg matches 0.. run scoreboard players set #luna dv.cfg 1
execute unless score #kevin dv.cfg matches 0.. run scoreboard players set #kevin dv.cfg 1
execute unless score #nicolas dv.cfg matches 0.. run scoreboard players set #nicolas dv.cfg 1
execute unless score #suenos dv.cfg matches 0.. run scoreboard players set #suenos dv.cfg 1
execute unless score #sane dv.dev matches -999999..999999 run scoreboard players set #sane dv.dev 1000
execute unless score #love dv.dev matches -999999..999999 run scoreboard players set #love dv.dev 0
execute unless score #stage dv.dev matches -999999..999999 run scoreboard players set #stage dv.dev 0
execute unless score #cd dv.dev matches -999999..999999 run scoreboard players set #cd dv.dev 120
execute unless score #lgen dv.dev matches -999999..999999 run scoreboard players set #lgen dv.dev 0
tellraw @a[scores={dv.debug=1}] {"text":"[Canon Event] cargado.","color":"dark_gray"}
