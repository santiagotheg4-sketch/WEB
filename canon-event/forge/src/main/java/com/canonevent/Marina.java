package com.canonevent;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.vehicle.Boat;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Criaturas del agua.
 * AHOGADA: una mujer pálida con el pelo mojado tapándole la cara. Se asoma del agua hasta el pecho y te mira; te llama
 * con la mano y con la voz («ven...»). Si la miras mucho rato se hunde. Si te metes al agua, nada hacia ti y te agarra
 * para hundirte. A veces está parada en la orilla, mirándote cuando vas en bote.
 * LEVIATAN: una serpiente enorme que da vueltas debajo de ti cuando estás en el mar; a veces saca el lomo,
 * mueve el bote, gime. Si estás nadando y pasa cerca, muerde.
 */
public class Marina extends Monster {
    public enum Tipo { AHOGADA, LEVIATAN }

    /** 0 asoma, 1 nada hacia ti, 2 te agarra, 3 se hunde, 4 parada en la orilla */
    private static final EntityDataAccessor<Integer> ESTADO = SynchedEntityData.defineId(Marina.class, EntityDataSerializers.INT);
    /** ticks que le quedan llamándote con la mano */
    private static final EntityDataAccessor<Integer> LLAMA = SynchedEntityData.defineId(Marina.class, EntityDataSerializers.INT);
    public final Tipo tipo;
    private int vida = 0, mirada = 0, cdVoz = 60, agarre = 0, hunde = 0, cdMordida = 0;
    private double angulo = 0, radio = 12, prof = 7, subida = 0;
    private boolean salio = false;

    public Marina(EntityType<? extends Monster> t, Level l, Tipo tipo) {
        super(t, l);
        this.tipo = tipo;
        this.xpReward = 0;
        this.setPersistenceRequired();
        this.addTag("dv_horror");
        this.addTag(tipo == Tipo.AHOGADA ? "dv_jahogada" : "dv_jleviatan");
        this.setCustomName(Component.literal(tipo == Tipo.AHOGADA ? "La Ahogada" : "Algo en el agua"));
        this.setCustomNameVisible(false);
        this.setNoGravity(true);
    }

    public static AttributeSupplier.Builder atributosAhogada() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 30).add(Attributes.MOVEMENT_SPEED, 0.25)
                .add(Attributes.ATTACK_DAMAGE, 3).add(Attributes.FOLLOW_RANGE, 64);
    }

    public static AttributeSupplier.Builder atributosLeviatan() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 600).add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ATTACK_DAMAGE, 6).add(Attributes.FOLLOW_RANGE, 96).add(Attributes.KNOCKBACK_RESISTANCE, 1.0);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(ESTADO, 0);
        this.entityData.define(LLAMA, 0);
    }

    public int estado() { return this.entityData.get(ESTADO); }
    public int llama() { return this.entityData.get(LLAMA); }
    void estado(int e) { this.entityData.set(ESTADO, e); }

    @Override
    protected void registerGoals() {
    }

    @Override public boolean removeWhenFarAway(double d) { return false; }
    @Override public boolean canBreatheUnderwater() { return true; }
    @Override public boolean isPushedByFluid() { return false; }
    @Override public boolean isPreventingPlayerRest(Player p) { return false; }

    void sonar(String id, float vol, float pitch) {
        this.level().playSound(null, getX(), getY(), getZ(), Monstruo.son(id), SoundSource.HOSTILE, vol, pitch);
    }

    void particulas(net.minecraft.core.particles.ParticleOptions p, int n, double dy, double r) {
        if (this.level() instanceof ServerLevel s) s.sendParticles(p, getX(), getY() + dy, getZ(), n, r, 0.2, r, 0.02);
    }

    /** Altura de la superficie del agua sobre esta columna (o NaN si no hay agua). */
    double superficie() {
        BlockPos p = blockPosition();
        Level l = this.level();
        int y = p.getY();
        if (!l.getFluidState(p).is(FluidTags.WATER)) {
            // busca agua debajo
            for (int i = 0; i < 4 && !l.getFluidState(p.below(i)).is(FluidTags.WATER); i++) y--;
            if (!l.getFluidState(new BlockPos(p.getX(), y, p.getZ())).is(FluidTags.WATER)) return Double.NaN;
        }
        while (y < l.getMaxBuildHeight() && l.getFluidState(new BlockPos(p.getX(), y + 1, p.getZ())).is(FluidTags.WATER)) y++;
        return y + 0.9;
    }

    Player cercano(double r) {
        return this.level().getNearestPlayer(getX(), getY(), getZ(), r, e -> e instanceof Player pl && !pl.isSpectator() && !pl.isCreative());
    }

    boolean meMira(Player p) {
        Vec3 ojo = p.getEyePosition();
        Vec3 a = new Vec3(getX() - ojo.x, getY() + getBbHeight() * 0.8 - ojo.y, getZ() - ojo.z);
        double d = a.length();
        if (d < 0.001) return true;
        return p.getViewVector(1.0f).dot(a.scale(1.0 / d)) > 0.93 && p.hasLineOfSight(this);
    }

    void mirarA(Entity e) {
        double dx = e.getX() - getX(), dz = e.getZ() - getZ();
        float yaw = (float) (Mth.atan2(dz, dx) * Mth.RAD_TO_DEG) - 90f;
        this.setYRot(Mth.rotLerp(0.2f, getYRot(), yaw));
        this.setYHeadRot(getYRot());
        this.yBodyRot = getYRot();
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        vida++;
        if (vida == 1 && getTags().contains("dv_orilla")) enOrilla();
        if (tipo == Tipo.LEVIATAN) { leviatan(); return; }
        ahogada();
    }

    @Override
    public void tick() {
        super.tick();
        if (!this.level().isClientSide) {
            int l = llama();
            if (l > 0) this.entityData.set(LLAMA, l - 1);
        }
    }

    // ------------------------------------------------------------ LA AHOGADA
    void ahogada() {
        Player p = cercano(96);
        if (p == null || vida > 20 * 200) { this.discard(); return; }
        double d = distanceTo(p);
        if (cdVoz > 0) cdVoz--;
        int e = estado();
        if (e != 2 && e != 3) mirarA(p);
        switch (e) {
            case 0 -> { // asomada: cabeza y hombros fuera del agua
                double s = superficie();
                if (Double.isNaN(s)) { estado(3); break; }
                double objetivoY = s - 1.25 + Mth.sin(vida * 0.08f) * 0.06;
                setDeltaMovement(0, (objetivoY - getY()) * 0.2, 0);
                if (meMira(p)) mirada++; else mirada = Math.max(0, mirada - 1);
                if (cdVoz == 0) llamar(p);
                if (mirada > 90) { estado(3); sonar("gen.susurro", 1.2f, 0.7f); }
                if (p.isInWater() && d < 18) { estado(1); sonar("mar.chapoteo", 1.5f, 0.7f); }
                else if (d < 6) estado(3); // te acercaste por tierra: se hunde
                if (vida % 30 == 0) particulas(ParticleTypes.DRIPPING_WATER, 4, 1.6, 0.3);
            }
            case 4 -> { // en la orilla, de pie, empapada
                setDeltaMovement(0, isInWater() ? 0.02 : -0.08, 0);
                if (cdVoz == 0) llamar(p);
                if (vida % 10 == 0) particulas(ParticleTypes.DRIPPING_WATER, 3, 1.4, 0.25);
                if (meMira(p)) mirada++; else mirada = Math.max(0, mirada - 1);
                if (d < 9 || mirada > 120) { estado(3); sonar("mar.chapoteo", 1.2f, 0.6f); }
            }
            case 1 -> { // nada hacia ti por debajo del agua
                if (!p.isInWater() && !(p.getVehicle() instanceof Boat)) {
                    if (d > 14) estado(3);
                }
                Vec3 obj = p.position().add(0, -0.6, 0);
                Vec3 dir = obj.subtract(position());
                double len = dir.length();
                double vel = isInWater() ? 0.24 : 0.08;
                if (len > 0.01) setDeltaMovement(dir.scale(Math.min(vel, len) / len));
                if (vida % 8 == 0) particulas(ParticleTypes.BUBBLE, 6, 0.6, 0.3);
                if (d < 1.6 && p.isInWater()) agarrar(p);
                if (vida % 40 == 0) sonar("gen.respira_lenta", 0.8f, 0.5f);
            }
            case 2 -> { // te agarra: te hunde
                agarre--;
                setPos(p.getX(), p.getY() - 1.0, p.getZ());
                setDeltaMovement(Vec3.ZERO);
                p.setDeltaMovement(p.getDeltaMovement().multiply(0.4, 0, 0.4).add(0, -0.09, 0));
                p.hurtMarked = true;
                if (agarre % 20 == 0) p.hurt(this.damageSources().mobAttack(this), 1.5f);
                if (agarre % 6 == 0) particulas(ParticleTypes.BUBBLE_COLUMN_UP, 8, 1.0, 0.3);
                if (agarre <= 0 || !p.isInWater()) soltar();
            }
            case 3 -> { // se hunde y desaparece
                hunde++;
                if (!isInWater()) { // en tierra: se desvanece
                    if (hunde % 3 == 0) particulas(ParticleTypes.FALLING_WATER, 10, 1.0, 0.3);
                    if (hunde > 20) { particulas(ParticleTypes.POOF, 20, 1.0, 0.3); this.discard(); }
                    break;
                }
                setDeltaMovement(0, -0.06, 0);
                if (hunde % 4 == 0) particulas(ParticleTypes.BUBBLE, 5, 1.2, 0.25);
                if (hunde > 50) this.discard();
            }
            default -> estado(0);
        }
    }

    void llamar(Player p) {
        cdVoz = 160 + this.random.nextInt(140);
        this.entityData.set(LLAMA, 60);
        String[] voces = {"mar.voz_ven", "mar.voz_tibia", "mar.voz_ayuda", "mar.voz_abajo", "mar.voz_nombre", "mar.canto"};
        sonar(voces[this.random.nextInt(voces.length)], 3.0f, 0.95f + this.random.nextFloat() * 0.1f);
        if (p instanceof ServerPlayer sp && this.random.nextInt(3) == 0)
            Monstruo.comando(sp, "title @s actionbar {\"text\":\"Alguien te llama desde el agua\",\"color\":\"#8fb8c9\",\"italic\":true}");
    }

    void agarrar(Player p) {
        estado(2);
        agarre = 70;
        sonar("mar.grito", 2.0f, 0.8f);
        p.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 70, 3, false, false));
        p.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 80, 0, false, false));
        if (p instanceof ServerPlayer sp) {
            Monstruo.comando(sp, "function canon:x/jumpscare");
            Monstruo.comando(sp, "scoreboard players add @s dv.miedo 20");
            Monstruo.comando(sp, "title @s actionbar {\"text\":\"¡TE ESTÁ HUNDIENDO! ¡PÉGALE!\",\"color\":\"#c94a4a\",\"bold\":true}");
        }
    }

    void soltar() {
        estado(3);
        hunde = 0;
        sonar("mar.chapoteo", 1.5f, 0.5f);
    }

    // ------------------------------------------------------------ EL LEVIATÁN
    void leviatan() {
        this.noPhysics = true; // es enorme: pasa por el fondo, las rocas y los corales
        Player p = cercano(120);
        if (p == null || vida > 20 * 60) { hundirseYIrse(p); return; }
        if (cdMordida > 0) cdMordida--;
        double s = superficie();
        if (Double.isNaN(s)) s = p.getY();
        // da vueltas alrededor tuyo, a veces sube a la superficie
        angulo += 0.045;
        radio = Math.max(3.5, radio + (salio ? 0.03 : -0.02));
        if (!salio && vida > 200 && this.random.nextInt(260) == 0) { subida = 1; sonar("mar.gemido", 8.0f, 0.6f); }
        if (subida > 0) {
            subida += 1;
            if (subida > 90) { subida = 0; salio = true; }
        }
        double alto = subida > 0 ? Math.sin(subida / 90.0 * Math.PI) * (prof - 0.6) : 0;
        Vec3 obj = new Vec3(p.getX() + Math.cos(angulo) * radio, s - prof + alto, p.getZ() + Math.sin(angulo) * radio);
        Vec3 dir = obj.subtract(position());
        setDeltaMovement(dir.scale(0.12));
        // mira hacia donde nada (tangente del círculo)
        float yaw = (float) (Mth.atan2(Math.cos(angulo), -Math.sin(angulo)) * Mth.RAD_TO_DEG) - 90f;
        setYRot(Mth.rotLerp(0.15f, getYRot(), yaw));
        yBodyRot = getYRot();
        setYHeadRot(getYRot());
        if (subida > 0 && subida % 5 == 0) particulas(ParticleTypes.SPLASH, 30, 2.4, 1.6);
        if (vida % 160 == 0) sonar("mar.gemido", 6.0f, 0.5f + this.random.nextFloat() * 0.2f);
        if (vida % 50 == 0) particulas(ParticleTypes.BUBBLE_COLUMN_UP, 12, 2.0, 1.0);
        double dh = Math.hypot(p.getX() - getX(), p.getZ() - getZ());
        // mece el bote cuando pasa por debajo
        if (p.getVehicle() instanceof Boat b && dh < 5 && vida % 20 == 0) {
            b.setDeltaMovement(b.getDeltaMovement().add((this.random.nextDouble() - 0.5) * 0.4, 0.25, (this.random.nextDouble() - 0.5) * 0.4));
            b.hurtMarked = true;
            sonar("mar.chapoteo", 2.0f, 0.5f);
            if (p instanceof ServerPlayer sp) Monstruo.comando(sp, "scoreboard players add @s dv.miedo 6");
        }
        // si estás nadando y pasa cerca, muerde y se va
        if (p.isInWater() && p.getVehicle() == null && distanceTo(p) < 4.5 && cdMordida == 0) {
            cdMordida = 400;
            p.hurt(this.damageSources().mobAttack(this), 7.0f);
            sonar("mar.grito", 2.5f, 0.4f);
            if (p instanceof ServerPlayer sp) {
                Monstruo.comando(sp, "function canon:x/jumpscare");
                Monstruo.comando(sp, "scoreboard players add @s dv.miedo 25");
            }
            vida = 20 * 60 - 60;
        }
    }

    void hundirseYIrse(Player p) {
        setDeltaMovement(0, -0.15, 0);
        hunde++;
        if (hunde > 60) this.discard();
    }

    @Override
    public boolean hurt(DamageSource s, float amt) {
        if (tipo == Tipo.LEVIATAN) return false;
        if (s.is(net.minecraft.tags.DamageTypeTags.IS_DROWNING)) return false;
        boolean r = super.hurt(s, amt);
        if (r && estado() != 3) { // le pegaste: te suelta y se va
            sonar("mar.grito", 1.4f, 1.3f);
            soltar();
        }
        return r;
    }

    @Override
    public void addAdditionalSaveData(CompoundTag t) {
        super.addAdditionalSaveData(t);
        t.putInt("CanonVida", vida);
        t.putInt("CanonEstado", estado());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag t) {
        super.readAdditionalSaveData(t);
        vida = t.getInt("CanonVida");
        estado(t.getInt("CanonEstado"));
    }

    /** Para invocarla parada en la orilla. */
    public void enOrilla() {
        estado(4);
        this.setNoGravity(false);
    }
}
