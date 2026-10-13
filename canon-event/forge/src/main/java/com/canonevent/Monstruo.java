package com.canonevent;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Monstruo del mod con inteligencia propia.
 * DIANA: se queda quieta si la miras, se acerca cuando no la miras, se esfuma si la miras mucho rato,
 * y de noche (o con mucho miedo) te persigue corriendo. Si te alcanza: susto y daño.
 * GIGANTE: camina lento a lo lejos; si lo miras se detiene y te mira; si te acercas, desaparece.
 */
public class Monstruo extends Monster {
    public enum Tipo { DIANA, GIGANTE }

    private static final EntityDataAccessor<Boolean> PERSIGUE = SynchedEntityData.defineId(Monstruo.class, EntityDataSerializers.BOOLEAN);
    public final Tipo tipo;
    private int vida = 0, visto = 0, persigueT = 0, cdGolpe = 0, cdSonido = 0;
    private Vec3 rumbo = null;

    public Monstruo(EntityType<? extends Monster> t, Level l, Tipo tipo) {
        super(t, l);
        this.tipo = tipo;
        this.xpReward = 0;
        this.setPersistenceRequired();
        this.addTag("dv_horror");
        this.addTag(tipo == Tipo.DIANA ? "dv_jdiana" : "dv_jgigante");
        this.setCustomName(Component.literal(tipo == Tipo.DIANA ? "Diana" : "El Gigante"));
        this.setCustomNameVisible(false);
    }

    public static AttributeSupplier.Builder atributosDiana() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 80).add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ATTACK_DAMAGE, 6).add(Attributes.FOLLOW_RANGE, 64).add(Attributes.KNOCKBACK_RESISTANCE, 1.0);
    }

    public static AttributeSupplier.Builder atributosGigante() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 400).add(Attributes.MOVEMENT_SPEED, 0.12)
                .add(Attributes.ATTACK_DAMAGE, 10).add(Attributes.FOLLOW_RANGE, 128).add(Attributes.KNOCKBACK_RESISTANCE, 1.0);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(PERSIGUE, false);
    }

    public boolean persigue() {
        return this.entityData.get(PERSIGUE);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
    }

    @Override
    public boolean removeWhenFarAway(double d) {
        return false;
    }

    static SoundEvent son(String id) {
        return SoundEvent.createVariableRangeEvent(new ResourceLocation("canon", id));
    }

    void sonar(String id, float vol, float pitch) {
        this.level().playSound(null, getX(), getY(), getZ(), son(id), SoundSource.HOSTILE, vol, pitch);
    }

    /** ¿El jugador me está mirando? */
    boolean meMira(Player p) {
        Vec3 ojo = p.getEyePosition();
        Vec3 a = new Vec3(getX() - ojo.x, getY() + getBbHeight() * 0.7 - ojo.y, getZ() - ojo.z);
        double d = a.length();
        if (d < 0.001) return true;
        double dot = p.getViewVector(1.0f).dot(a.scale(1.0 / d));
        return dot > (tipo == Tipo.GIGANTE ? 0.9 : 0.8) && p.hasLineOfSight(this);
    }

    void esfumar() {
        if (this.level() instanceof ServerLevel s) {
            s.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY() + 1.5, getZ(), 40, 0.4, 1.0, 0.4, 0.02);
            s.sendParticles(ParticleTypes.SOUL, getX(), getY() + 1.5, getZ(), 15, 0.3, 0.8, 0.3, 0.02);
        }
        sonar(tipo == Tipo.DIANA ? "diana.scream" : "gen.drone_grave", 1.0f, tipo == Tipo.DIANA ? 0.6f : 0.5f);
        this.discard();
    }

    static void comando(ServerPlayer p, String c) {
        p.getServer().getCommands().performPrefixedCommand(p.createCommandSourceStack().withSuppressedOutput().withPermission(4), c);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        vida++;
        if (cdGolpe > 0) cdGolpe--;
        if (cdSonido > 0) cdSonido--;
        Player p = this.level().getNearestPlayer(getX(), getY(), getZ(), tipo == Tipo.GIGANTE ? 160 : 64,
                e -> e instanceof Player pl && !pl.isSpectator() && !pl.isCreative());
        if (p == null) {
            if (vida > 200) this.discard();
            return;
        }
        double d = distanceTo(p);
        boolean mira = meMira(p);
        if (tipo == Tipo.GIGANTE) {
            gigante(p, d, mira);
            return;
        }
        // ---------------- DIANA
        if (vida > 20 * 150) { esfumar(); return; }
        this.getLookControl().setLookAt(p, 30f, 30f);
        boolean noche = !this.level().isDay();
        if (!persigue() && noche && d < 18 && this.random.nextInt(500) == 0) empezarPersecucion();
        if (persigue()) {
            persigueT++;
            this.getNavigation().moveTo(p, 1.75);
            if (persigueT > 20 * 20) { esfumar(); return; }
        } else if (mira) {
            visto++;
            this.getNavigation().stop();
            if (visto == 1 && cdSonido == 0) { sonar("gen.respira_lenta", 0.8f, 0.8f); cdSonido = 120; }
            if (visto > 40) { esfumar(); return; }
        } else {
            visto = 0;
            if (d > 2.2) this.getNavigation().moveTo(p, d > 12 ? 1.6 : 1.1);
            if (cdSonido == 0 && this.random.nextInt(40) == 0) { sonar("gen.susurro", 0.7f, 0.9f); cdSonido = 80; }
        }
        if (d < 2.0 && cdGolpe == 0 && (!mira || persigue())) atrapar(p);
    }

    void empezarPersecucion() {
        this.entityData.set(PERSIGUE, true);
        persigueT = 0;
        sonar("diana.scream", 1.2f, 0.7f);
    }

    void atrapar(Player p) {
        cdGolpe = 40;
        p.hurt(this.damageSources().mobAttack(this), 6.0f);
        if (p instanceof ServerPlayer sp) {
            comando(sp, "function canon:x/jumpscare");
            comando(sp, "scoreboard players add @s dv.miedo 25");
        }
        esfumar();
    }

    void gigante(Player p, double d, boolean mira) {
        if (vida > 20 * 180 || d < 22) { esfumar(); return; }
        if (rumbo == null) {
            double a = this.random.nextDouble() * Math.PI * 2;
            rumbo = new Vec3(Math.cos(a), 0, Math.sin(a));
        }
        if (mira) {
            visto++;
            this.getNavigation().stop();
            if (visto > 40) this.getLookControl().setLookAt(p, 10f, 10f);
        } else {
            visto = Math.max(0, visto - 1);
            Vec3 obj = position().add(rumbo.scale(6));
            this.getNavigation().moveTo(obj.x, obj.y, obj.z, 0.8);
        }
        if (this.tickCount % 30 == 0) sonar("gen.golpe1", 6.0f, 0.4f);
        // ruge desde lejos: grave, todo tiembla, y uno lo busca con la mirada (la cámara no se mueve sola)
        if (vida == 20 || (vida > 200 && this.random.nextInt(500) == 0)) rugir();
    }

    void rugir() {
        sonar("gen.rugido_gigante", 16.0f, 0.75f + this.random.nextFloat() * 0.1f);
        for (Player pl : this.level().players())
            if (pl instanceof ServerPlayer sp && pl.distanceTo(this) < 260)
                comando(sp, "scoreboard players set @s dv.shake " + (pl.distanceTo(this) < 120 ? 60 : 35));
    }

    @Override
    public boolean hurt(DamageSource s, float amt) {
        if (tipo == Tipo.GIGANTE) return false;
        boolean r = super.hurt(s, amt * 0.35f);
        if (r && this.random.nextInt(3) == 0) esfumar();
        return r;
    }

    @Override
    public boolean isPreventingPlayerRest(Player p) {
        return tipo == Tipo.DIANA;
    }

    @Override
    public void addAdditionalSaveData(CompoundTag t) {
        super.addAdditionalSaveData(t);
        t.putInt("CanonVida", vida);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag t) {
        super.readAdditionalSaveData(t);
        vida = t.getInt("CanonVida");
    }

    @Override
    protected void playStepSound(net.minecraft.core.BlockPos pos, net.minecraft.world.level.block.state.BlockState st) {
        if (tipo == Tipo.GIGANTE) return;
        this.playSound(son("gen.paso_madera"), 0.5f, 0.7f);
    }
}
