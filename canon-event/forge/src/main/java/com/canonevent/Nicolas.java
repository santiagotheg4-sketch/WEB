package com.canonevent;

import net.minecraft.commands.arguments.EntityAnchorArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Nicolás, el de las cuevas. Ya no camina a través de las paredes: busca el camino de verdad.
 * Cada vez que aparece hace algo distinto (y nunca rompe bloques):
 * ACECHA (te sigue de lejos y se esconde si lo miras), TECHO (pegado al techo, boca abajo; cae delante de ti),
 * CORRE (te persigue riéndose), APAGA (te apaga las antorchas una por una), PICA (pica la piedra detrás de la pared
 * hasta abrir un hueco y mirarte por él). Si le pegas, se ríe y huye a la oscuridad.
 */
public class Nicolas extends Monster {
    public static final int ACECHA = 0, TECHO = 1, CORRE = 2, APAGA = 3, PICA = 4, HUYE = 5, ESCONDE = 6, LEJOS = 7, AGARRA = 8, PREVIO = 9;
    private static final EntityDataAccessor<Integer> ESTADO = SynchedEntityData.defineId(Nicolas.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Integer> CARA = SynchedEntityData.defineId(Nicolas.class, EntityDataSerializers.INT);
    static final String[] INSULTOS = {"Nadie te va a extrañar aquí abajo.", "Cava, cava... estás cavando tu propia tumba.",
            "Aquí abajo nadie oye tus gritos.", "Eres lento. Eres débil. Eres mío.", "Tus amigos ya se fueron sin ti.", "Hueles a miedo.",
            "¿Por qué sigues intentando? Ya perdiste.", "Te vi. Te vi. Te vi.", "Apaga la luz. Así es más divertido.",
            "Estoy detrás de la pared. Escucha.", "Corre, gordito... ah no, ese soy yo. Jajaja.", "Sigue bajando. Abajo te espero."};
    private int vida = 0, t = 0, visto = 0, cdHabla = 100, cdGolpe = 0, apagadas = 0, golpes = 0;
    private BlockPos hueco = null;
    private int previo = 0, elegido = ACECHA;
    static final String[] VOCES = {"gen.voz_nico_te_veo", "gen.voz_nico_baja", "gen.voz_nico_buscas", "gen.voz_nico_ven", "gen.voz_nicolas_aqui"};

    public Nicolas(EntityType<? extends Monster> tipo, Level l) {
        super(tipo, l);
        this.xpReward = 0;
        this.setPersistenceRequired();
        this.addTag("dv_horror");
        this.addTag("dv_jnicolas");
        this.setCustomName(Component.literal("Nicolás"));
        this.setCustomNameVisible(false);
    }

    public static AttributeSupplier.Builder atributos() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 40).add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ATTACK_DAMAGE, 4).add(Attributes.FOLLOW_RANGE, 64);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(ESTADO, ACECHA);
        this.entityData.define(CARA, 0);
    }

    public int estado() { return this.entityData.get(ESTADO); }
    public int cara() { return this.entityData.get(CARA); }
    void cara(int c) { this.entityData.set(CARA, c); }

    void estado(int e) {
        this.entityData.set(ESTADO, e);
        t = 0;
        visto = 0;
        this.setNoGravity(e == TECHO);
        if (e != TECHO) this.getNavigation().stop();
    }

    @Override protected void registerGoals() { this.goalSelector.addGoal(0, new FloatGoal(this)); }
    @Override public boolean removeWhenFarAway(double d) { return false; }
    @Override public boolean isPreventingPlayerRest(Player p) { return true; }

    void sonar(String id, float vol, float pitch) {
        this.level().playSound(null, getX(), getY(), getZ(), Monstruo.son(id), SoundSource.HOSTILE, vol, pitch);
    }

    void humo(int n) {
        if (this.level() instanceof ServerLevel s) s.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY() + 1, getZ(), n, 0.3, 0.7, 0.3, 0.01);
    }

    Player victima() {
        return this.level().getNearestPlayer(getX(), getY(), getZ(), 56, e -> e instanceof Player pl && !pl.isSpectator() && !pl.isCreative());
    }

    boolean meMira(Player p) {
        Vec3 ojo = p.getEyePosition();
        Vec3 a = getEyePosition().subtract(ojo);
        double d = a.length();
        return d < 0.01 || (p.getViewVector(1f).dot(a.scale(1 / d)) > 0.85 && p.hasLineOfSight(this));
    }

    /** Le gira la cámara al jugador para que vea a Nicolás a la cara (justo a sus ojos). */
    void mirame(Player p) {
        if (p instanceof ServerPlayer sp) sp.lookAt(EntityAnchorArgument.Anchor.EYES, getEyePosition());
    }

    void decir(Player p, String txt) {
        if (p instanceof ServerPlayer sp)
            Monstruo.comando(sp, "tellraw @a[distance=..48] [{\"text\":\"Nicolás: \",\"color\":\"#8a8a96\",\"bold\":true},{\"text\":\"" + txt + "\",\"color\":\"#b9b9c6\",\"italic\":true}]");
    }

    /** Elige qué hace esta vez. */
    public void empezar() {
        if (getTags().contains("dv_nagarra")) { estado(AGARRA); setNoGravity(true); noPhysics = true; cara(0); return; }
        int[] opciones = {LEJOS, LEJOS, ACECHA, ACECHA, TECHO, CORRE, APAGA, PICA};
        int e = opciones[this.random.nextInt(opciones.length)];
        if (getTags().contains("dv_nlejos")) e = LEJOS;
        if (getTags().contains("dv_ntecho")) e = TECHO;
        if (getTags().contains("dv_ncorre")) e = CORRE;
        if (getTags().contains("dv_napaga")) e = APAGA;
        if (getTags().contains("dv_npica")) e = PICA;
        Player p = victima();
        if (e == TECHO && (p == null || !alTecho(p))) e = ACECHA;
        if (e == PICA && (p == null || !aLaPared(p))) e = ACECHA;
        // nada aparece de golpe: primero se le oye un rato (pasos con eco, risas lejos, respiración) y luego aparece
        boolean directo = getTags().stream().anyMatch(t -> t.startsWith("dv_n"));
        if (!directo && e != TECHO && e != PICA) {
            elegido = e;
            previo = 160 + this.random.nextInt(240);
            estado(PREVIO);
            this.setInvisible(true);
            this.noPhysics = true;
            this.setNoGravity(true);
            return;
        }
        if (e != TECHO) estado(e);
        if (e == CORRE) arrancar(p);
    }

    void previo(Player p) {
        setDeltaMovement(Vec3.ZERO);
        this.getNavigation().stop();
        if (p instanceof ServerPlayer sp) {
            int r = this.random.nextInt(100);
            if (t % 45 == 0) Monstruo.comando(sp, "playsound canon:gen.paso_tierra hostile @s ^" + (this.random.nextInt(9) - 4) + " ^ ^-" + (6 + this.random.nextInt(6)) + " 0.5 0.8");
            if (t == previo / 2) Monstruo.comando(sp, "playsound canon:nicolas.risa hostile @s ^-10 ^ ^-6 0.35 0.7");
            if (t == previo - 40) Monstruo.comando(sp, "playsound " + "canon:" + VOCES[this.random.nextInt(VOCES.length)] + " hostile @s ^4 ^ ^-8 0.6 0.9");
            if (r == 0) Monstruo.comando(sp, "playsound canon:gen.respira_lenta hostile @s ^ ^ ^-3 0.4 0.8");
        }
        if (t >= previo) {
            this.setInvisible(false);
            this.noPhysics = false;
            this.setNoGravity(false);
            int e = elegido;
            if (e == LEJOS) { if (!aLoLejos(p)) e = ACECHA; }
            estado(e);
            if (e == LEJOS) setNoGravity(false);
            if (e == CORRE) arrancar(p);
        }
    }

    // --- te mira desde lejos, en la oscuridad, con los ojos blancos
    boolean aLoLejos(Player p) {
        for (int i = 0; i < 30; i++) {
            double a = this.random.nextDouble() * Math.PI * 2, r = 16 + this.random.nextInt(14);
            BlockPos b = BlockPos.containing(p.getX() + Math.cos(a) * r, p.getY() + this.random.nextInt(7) - 3, p.getZ() + Math.sin(a) * r);
            for (int k = 0; k < 6; k++, b = b.below()) {
                if (this.level().getBlockState(b).isAir() && this.level().getBlockState(b.above()).isAir() && this.level().getBlockState(b.below()).isSolid()) {
                    Vec3 pos = Vec3.atBottomCenterOf(b);
                    HitResult h = this.level().clip(new ClipContext(p.getEyePosition(), pos.add(0, 1.6, 0), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
                    if (h.getType() != HitResult.Type.MISS) break;
                    if (this.level().getMaxLocalRawBrightness(b) > 7) break;
                    moveTo(pos.x, pos.y, pos.z, 0, 0);
                    return true;
                }
            }
        }
        return false;
    }

    void lejos(Player p, double d) {
        this.getNavigation().stop();
        if (meMira(p)) visto++;
        if (t % 90 == 30 && this.random.nextInt(2) == 0) sonar(VOCES[this.random.nextInt(VOCES.length)], 2.2f, 0.9f);
        if (t % 140 == 70) sonar("nicolas.risa", 1.6f, 0.75f);
        if (d < 10 || visto > 140 || t > 20 * 45) {
            // se va caminando de espaldas hacia lo oscuro y desaparece
            Vec3 lejos = position().add(position().subtract(p.position()).normalize().scale(8));
            estado(HUYE);
            this.getNavigation().moveTo(lejos.x, lejos.y, lejos.z, 0.7);
        }
    }

    // --- picabas y, al romper el bloque, está ahí: agarrado de los bordes, mirándote por el hueco
    void agarra(Player p) {
        setDeltaMovement(Vec3.ZERO);
        if (t == 1) {
            sonar("nicolas.risa", 0.7f, 0.6f);
            if (p instanceof ServerPlayer sp) {
                Monstruo.comando(sp, "playsound canon:gen.stinger hostile @s ~ ~ ~ 0.9 0.7");
                Monstruo.comando(sp, "scoreboard players add @s dv.miedo 20");
            }
        }
        if (t == 30) sonar(VOCES[this.random.nextInt(VOCES.length)], 1.2f, 0.85f);
        if (t == 45) cara(2);
        if (meMira(p)) visto++;
        if (visto > 40 || t > 90) {
            sonar("nicolas.risa", 1.0f, 1.2f);
            humo(10);
            this.discard();
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        vida++;
        t++;
        if (vida == 1) empezar();
        if (cdHabla > 0) cdHabla--;
        if (cdGolpe > 0) cdGolpe--;
        Player p = victima();
        if (p == null || vida > 20 * 120) { irse(); return; }
        double d = distanceTo(p);
        if (estado() != HUYE && estado() != TECHO && estado() != AGARRA) this.getLookControl().setLookAt(p, 30f, 30f);
        if (cdHabla == 0 && estado() != PICA && estado() != TECHO && estado() != PREVIO && estado() != AGARRA && estado() != LEJOS) {
            cdHabla = 220 + this.random.nextInt(200);
            decir(p, INSULTOS[this.random.nextInt(INSULTOS.length)]);
            cara(this.random.nextBoolean() ? 0 : 1);
        }
        switch (estado()) {
            case ACECHA -> acecha(p, d);
            case ESCONDE -> { if (this.getNavigation().isDone() || t > 80) estado(ACECHA); }
            case TECHO -> techo(p, d);
            case CORRE -> corre(p, d);
            case APAGA -> apaga(p, d);
            case PICA -> pica(p, d);
            case HUYE -> { if (t > 50 || this.getNavigation().isDone()) irse(); }
            case LEJOS -> lejos(p, d);
            case AGARRA -> agarra(p);
            case PREVIO -> previo(p);
            default -> estado(ACECHA);
        }
    }

    // --- te sigue de lejos; si lo miras, se esconde detrás de algo
    void acecha(Player p, double d) {
        if (meMira(p)) {
            visto++;
            if (visto == 1) sonar("nicolas.risa", 0.6f, 0.8f);
            if (visto > 12) esconderse(p);
            this.getNavigation().stop();
            return;
        }
        visto = 0;
        if (t % 10 == 0 && d > 9) this.getNavigation().moveTo(p, 0.85);
        if (d < 9) this.getNavigation().stop();
        if (t % 50 == 0) sonar("nicolas.pasos", 0.9f, 0.9f);
        if (t > 600 || (t > 200 && this.random.nextInt(300) == 0)) {
            if (this.random.nextBoolean()) arrancar(p); else irse();
        }
    }

    void esconderse(Player p) {
        for (int i = 0; i < 16; i++) {
            Vec3 lejos = position().subtract(p.position()).normalize();
            double ang = (this.random.nextDouble() - 0.5) * 2.4;
            Vec3 dir = new Vec3(lejos.x * Math.cos(ang) - lejos.z * Math.sin(ang), 0, lejos.x * Math.sin(ang) + lejos.z * Math.cos(ang));
            Vec3 obj = position().add(dir.scale(5 + this.random.nextInt(6)));
            HitResult h = this.level().clip(new ClipContext(p.getEyePosition(), obj.add(0, 1.5, 0), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
            if (h.getType() == HitResult.Type.BLOCK && this.getNavigation().moveTo(obj.x, obj.y, obj.z, 1.25)) {
                estado(ESCONDE);
                return;
            }
        }
        irse(); // no encontró dónde esconderse: se esfuma
    }

    // --- pegado al techo, boca abajo
    boolean alTecho(Player p) {
        Vec3 v = p.getViewVector(1f);
        Vec3 h = new Vec3(v.x, 0, v.z).normalize();
        for (int dist : new int[]{7, 6, 8, 5}) {
            Vec3 base = p.position().add(h.scale(dist));
            BlockPos b = BlockPos.containing(base);
            for (int up = 2; up <= 6; up++) {
                BlockPos c = b.above(up);
                if (!this.level().getBlockState(c).isAir()) {
                    if (up < 3) break;
                    double y = c.getY() - getBbHeight();
                    moveTo(base.x, y, base.z, p.getYRot() + 180, 0);
                    estado(TECHO);
                    setDeltaMovement(Vec3.ZERO);
                    return true;
                }
            }
        }
        return false;
    }

    void techo(Player p, double d) {
        setDeltaMovement(Vec3.ZERO);
        double dh = Math.hypot(p.getX() - getX(), p.getZ() - getZ());
        if (meMira(p)) visto++;
        if (t % 40 == 0) sonar("gen.respira_lenta", 0.7f, 0.7f);
        if (dh < 2.5 || visto > 25) { // cae delante de ti
            cara(2);
            estado(CORRE);
            setDeltaMovement(0, -0.4, 0);
            sonar("nicolas.maldito", 1.4f, 0.9f);
            if (p instanceof ServerPlayer sp) {
                Monstruo.comando(sp, "function canon:x/jumpscare");
                Monstruo.comando(sp, "scoreboard players add @s dv.miedo 20");
            }
            mirame(p);
            arrancar(p);
        }
        if (t > 900) irse();
    }

    // --- te persigue
    void arrancar(Player p) {
        estado(CORRE);
        cara(2);
        sonar("nicolas.risa", 1.4f, 1.1f);
        if (p instanceof ServerPlayer sp) Monstruo.comando(sp, "title @s actionbar {\"text\":\"¡CORRE!\",\"color\":\"#b01212\",\"bold\":true}");
    }

    void corre(Player p, double d) {
        if (t % 6 == 0) this.getNavigation().moveTo(p, d > 14 ? 1.25 : 1.1);
        if (t % 24 == 0) sonar("nicolas.pasos", 1.2f, 1.2f);
        if (t % 70 == 0) sonar("nicolas.risa", 1.2f, 0.9f + this.random.nextFloat() * 0.3f);
        if (d < 1.8 && cdGolpe == 0) {
            cdGolpe = 30;
            this.swing(InteractionHand.MAIN_HAND);
            p.hurt(this.damageSources().mobAttack(this), 4f);
            p.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 60, 0, false, false));
            sonar("nicolas.maldito", 1.4f, 1f);
            if (p instanceof ServerPlayer sp) {
                Monstruo.comando(sp, "function canon:x/jumpscare");
                Monstruo.comando(sp, "scoreboard players add @s dv.miedo 15");
            }
            mirame(p);
            golpes++;
            if (golpes >= 2) irse();
        }
        if (t > 20 * 15) irse();
    }

    // --- te apaga las antorchas
    void apaga(Player p, double d) {
        if (t % 10 == 0 && d > 8) this.getNavigation().moveTo(p, 0.9);
        if (t % 18 != 0) return;
        BlockPos c = p.blockPosition();
        BlockPos mejor = null;
        double best = 1e9;
        for (BlockPos b : BlockPos.betweenClosed(c.offset(-10, -4, -10), c.offset(10, 5, 10))) {
            BlockState s = this.level().getBlockState(b);
            if (s.is(Blocks.TORCH) || s.is(Blocks.WALL_TORCH) || s.is(Blocks.SOUL_TORCH) || s.is(Blocks.SOUL_WALL_TORCH)
                    || s.is(Blocks.LANTERN) || s.is(Blocks.SOUL_LANTERN)) {
                double dd = b.distSqr(c);
                if (dd > 4 && dd < best) { best = dd; mejor = b.immutable(); }
            }
        }
        if (mejor != null && apagadas < 8) {
            this.level().removeBlock(mejor, false);
            this.level().playSound(null, mejor, SoundEvents.FIRE_EXTINGUISH, SoundSource.BLOCKS, 0.8f, 0.7f);
            if (this.level() instanceof ServerLevel s) s.sendParticles(ParticleTypes.SMOKE, mejor.getX() + 0.5, mejor.getY() + 0.6, mejor.getZ() + 0.5, 10, 0.1, 0.1, 0.1, 0.01);
            apagadas++;
            if (apagadas == 1) decir(p, "Apaga la luz. Así es más divertido.");
        } else if (t > 100) {
            sonar("nicolas.risa", 1.0f, 0.7f);
            if (this.random.nextBoolean()) arrancar(p); else irse();
        }
    }

    // --- pica la pared detrás de ti hasta abrir un hueco y mirarte
    boolean aLaPared(Player p) {
        BlockPos c = p.blockPosition();
        for (int i = 0; i < 20; i++) {
            BlockPos w = c.offset(this.random.nextInt(9) - 4, this.random.nextInt(2), this.random.nextInt(9) - 4);
            BlockState s = this.level().getBlockState(w);
            if (!s.isSolid() || s.getDestroySpeed(this.level(), w) < 0 || s.getDestroySpeed(this.level(), w) > 50) continue;
            // detrás del bloque (lejos del jugador) tiene que caber Nicolás
            Vec3 dir = Vec3.atCenterOf(w).subtract(p.position()).normalize();
            BlockPos atras = BlockPos.containing(Vec3.atCenterOf(w).add(dir.x * 1.5, 0, dir.z * 1.5));
            if (atras.equals(w) || !this.level().getBlockState(atras).isAir() || !this.level().getBlockState(atras.above()).isAir()) continue;
            hueco = w;
            // se queda escondido dentro de la piedra (no se ve) mientras pica
            moveTo(atras.getX() + 0.5, atras.getY(), atras.getZ() + 0.5, 0, 0);
            this.setInvisible(true);
            this.noPhysics = true;
            this.setNoGravity(true);
            return true;
        }
        return false;
    }

    void pica(Player p, double d) {
        if (hueco == null) { irse(); return; }
        setDeltaMovement(Vec3.ZERO);
        if (t % 9 == 0 && t < 160) {
            this.level().playSound(null, hueco, SoundEvents.STONE_HIT, SoundSource.BLOCKS, 1.4f, 0.7f + this.random.nextFloat() * 0.2f);
            if (t % 45 == 0) this.level().playSound(null, hueco, SoundEvents.STONE_BREAK, SoundSource.BLOCKS, 0.8f, 0.6f);
        }
        if (t == 80 && p instanceof ServerPlayer sp)
            Monstruo.comando(sp, "title @s actionbar {\"text\":\"Alguien está picando la piedra... del otro lado\",\"color\":\"#8a8a96\",\"italic\":true}");
        // él no rompe nada: solo golpea la piedra del otro lado, se ríe bajito... y se va
        if (t == 170) {
            sonar("nicolas.risa", 0.6f, 0.7f);
            decir(p, "Sigue picando. Ya casi llegas a mí.");
        }
        if (t > 200) this.discard();
    }

    void irse() {
        humo(25);
        sonar("nicolas.risa", 0.9f, 0.7f);
        this.discard();
    }

    @Override
    public boolean hurt(DamageSource s, float amt) {
        if ((estado() == PICA || estado() == PREVIO) && isInvisible()) return false;
        if (estado() == AGARRA) { sonar("nicolas.risa", 1.2f, 1.3f); humo(10); this.discard(); return false; }
        boolean r = super.hurt(s, amt);
        if (r && estado() != HUYE && isAlive()) { // le pegaste: se ríe y huye a la oscuridad
            sonar("nicolas.risa", 1.3f, 1.3f);
            Player p = victima();
            if (p != null) {
                Vec3 lejos = position().add(position().subtract(p.position()).normalize().scale(14));
                estado(HUYE);
                this.getNavigation().moveTo(lejos.x, lejos.y, lejos.z, 1.4);
            }
        }
        return r;
    }

    @Override
    public void die(DamageSource s) {
        humo(40);
        sonar("nicolas.risa", 1.2f, 0.6f);
        super.die(s);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("CanonVida", vida);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        vida = tag.getInt("CanonVida");
        if (vida > 0) vida = 20 * 119; // al cargar el mundo se va pronto
    }

    @Override
    protected void playStepSound(BlockPos pos, BlockState st) {
        this.playSound(Monstruo.son("gen.paso_madera"), 0.4f, 0.8f);
    }
}
