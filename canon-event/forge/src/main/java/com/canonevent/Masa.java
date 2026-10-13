package com.canonevent;

import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
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
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;

/**
 * La Masa: la cosa de las catacumbas. Grande (3 bloques), camina en cuatro patas con brazos larguísimos,
 * y persigue de verdad: busca el camino por los pasillos, no atraviesa paredes.
 * Primero acecha despacio, después ruge y corre un poquito más lento que tú corriendo.
 * Si te alcanza te golpea y se detiene a rugir: es tu momento de escapar.
 */
public class Masa extends Monster {
    private static final EntityDataAccessor<Boolean> CORRE = SynchedEntityData.defineId(Masa.class, EntityDataSerializers.BOOLEAN);
    private int vida = 0, cdGolpe = 0, pausa = 0, sinVer = 0, atascado = 0;
    private net.minecraft.world.phys.Vec3 antes = null;

    public Masa(EntityType<? extends Monster> t, Level l) {
        super(t, l);
        this.xpReward = 0;
        this.setPersistenceRequired();
        this.setMaxUpStep(1.0f);
        this.addTag("dv_horror");
        this.addTag("dv_jmasa");
        this.setCustomName(Component.literal("La Masa"));
        this.setCustomNameVisible(false);
    }

    public static AttributeSupplier.Builder atributos() {
        return Monster.createMonsterAttributes().add(Attributes.MAX_HEALTH, 500).add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ATTACK_DAMAGE, 5).add(Attributes.FOLLOW_RANGE, 96).add(Attributes.KNOCKBACK_RESISTANCE, 1.0);
    }

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(CORRE, false);
    }

    public boolean corre() {
        return this.entityData.get(CORRE);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
    }

    @Override
    public boolean removeWhenFarAway(double d) {
        return false;
    }

    void sonar(String id, float vol, float pitch) {
        this.level().playSound(null, getX(), getY(), getZ(), Monstruo.son(id), SoundSource.HOSTILE, vol, pitch);
    }

    /** A quién persigue: primero a los que están en las catacumbas con Kevin, si no al jugador más cercano. */
    Player objetivo() {
        Player p = this.level().getNearestPlayer(getX(), getY(), getZ(), 80,
                e -> e instanceof Player pl && !pl.isSpectator() && !pl.isCreative() && pl.getTags().contains("dv_kpart"));
        if (p == null)
            p = this.level().getNearestPlayer(getX(), getY(), getZ(), 40, e -> e instanceof Player pl && !pl.isSpectator() && !pl.isCreative());
        return p;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        vida++;
        if (cdGolpe > 0) cdGolpe--;
        Player p = objetivo();
        if (p == null) {
            this.getNavigation().stop();
            if (vida > 600) this.discard();
            return;
        }
        double d = distanceTo(p);
        this.getLookControl().setLookAt(p, 20f, 20f);
        boolean ve = this.hasLineOfSight(p);
        sinVer = ve ? 0 : sinVer + 1;

        // fase 1: acecha despacio y respira; fase 2: ruge y corre
        if (!corre() && (vida > 160 || d < 7)) {
            this.entityData.set(CORRE, true);
            sonar("masa.rugido", 2.0f, 0.6f);
            if (p instanceof ServerPlayer sp) {
                Monstruo.comando(sp, "title @a[tag=dv_kpart] times 0 30 10");
                Monstruo.comando(sp, "title @a[tag=dv_kpart] title {\"text\":\"¡CORRE!\",\"color\":\"#c94a4a\",\"bold\":true}");
            }
        }
        if (pausa > 0) {
            // después de golpear se queda rugiendo, sacudiéndose: es cuando puedes huir
            pausa--;
            this.getNavigation().stop();
            if (pausa == 10) sonar("masa.rugido", 1.6f, 0.9f);
        } else if (this.tickCount % 5 == 0) {
            double vel;
            if (!corre()) vel = 0.72;
            else if (d > 24 || sinVer > 100) vel = 1.32;   // te pierde de vista: acelera para alcanzarte
            else if (d < 6) vel = 1.05;                     // muy cerca: si corres, te le escapas
            else vel = 1.12;
            this.getNavigation().moveTo(p, vel);
        }

        // sonidos y rastro
        boolean mueve = this.getDeltaMovement().horizontalDistanceSqr() > 0.002;
        if (mueve && this.tickCount % (corre() ? 9 : 16) == 0) {
            sonar("masa.arrastre", corre() ? 1.6f : 1.0f, 0.8f + this.random.nextFloat() * 0.3f);
            sonar("gen.golpe1", 0.7f, 0.5f);
        }
        if (this.tickCount % 70 == 0 && this.random.nextInt(2) == 0) sonar("gen.respira_lenta", 1.4f, 0.55f);
        if (corre() && this.tickCount % 120 == 0 && this.random.nextInt(3) == 0) sonar("masa.rugido", 1.8f, 0.7f + this.random.nextFloat() * 0.2f);
        if (this.level() instanceof ServerLevel s && this.tickCount % 6 == 0)
            s.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, Blocks.REDSTONE_BLOCK.defaultBlockState()),
                    getX(), getY() + 0.4, getZ(), 3, 0.6, 0.2, 0.6, 0);

        // si se atasca en una esquina y no la ves, «encuentra otro camino»: aparece en tu rastro, detrás de ti
        if (corre() && this.tickCount % 20 == 0) {
            net.minecraft.world.phys.Vec3 ahora = position();
            if (antes != null && antes.distanceTo(ahora) < 0.6 && d > 4 && pausa == 0) atascado++; else atascado = 0;
            antes = ahora;
            if (atascado >= 4 && !ve) {
                net.minecraft.world.phys.Vec3 t = Rastro.detrasDe(p.getUUID(), 14);
                if (t != null && p.position().distanceTo(t) > 8) {
                    this.teleportTo(t.x, t.y, t.z);
                    this.getNavigation().stop();
                    sonar("masa.arrastre", 1.6f, 0.6f);
                }
                atascado = 0;
            }
        }
        if (d < 2.4 && cdGolpe == 0 && pausa == 0 && ve) golpear(p);
    }

    void golpear(Player p) {
        cdGolpe = 50;
        pausa = 28;
        this.swing(InteractionHand.MAIN_HAND);
        p.hurt(this.damageSources().mobAttack(this), 5.0f);
        p.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 1, false, false));
        p.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 60, 0, false, false));
        sonar("masa.rugido", 2.0f, 1.2f);
        if (p instanceof ServerPlayer sp) {
            Monstruo.comando(sp, "scoreboard players add @s dv.miedo 15");
            Monstruo.comando(sp, "playsound canon:gen.stinger hostile @s ~ ~ ~ 1 0.8");
            Monstruo.comando(sp, "execute as @e[type=zombie,tag=dv_kevin,distance=..30] run tellraw @a[tag=dv_kpart] {\"text\":\"Kevin: ¡NOOO! ¡LEVÁNTATE! ¡CORRE!\",\"color\":\"#ffb347\",\"bold\":true}");
        }
    }

    @Override
    public boolean hurt(DamageSource s, float amt) {
        if (s.is(net.minecraft.tags.DamageTypeTags.IS_FALL) || s.is(net.minecraft.tags.DamageTypeTags.IS_FIRE)) return false;
        boolean r = super.hurt(s, amt * 0.1f);
        if (r && this.random.nextInt(3) == 0) sonar("masa.rugido", 1.5f, 1.4f);
        return r;
    }

    @Override
    public boolean isPreventingPlayerRest(Player p) {
        return true;
    }

    @Override
    public void addAdditionalSaveData(net.minecraft.nbt.CompoundTag t) {
        super.addAdditionalSaveData(t);
        t.putInt("CanonVida", vida);
    }

    @Override
    public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag t) {
        super.readAdditionalSaveData(t);
        vida = t.getInt("CanonVida");
    }

    @Override
    protected void playStepSound(net.minecraft.core.BlockPos pos, net.minecraft.world.level.block.state.BlockState st) {
    }
}
