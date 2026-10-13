package com.canonevent;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.Wolf;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.LivingAttackEvent;
import net.minecraftforge.event.entity.living.LivingChangeTargetEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Luna es una perrita, no una cazafantasmas: solo ataca vacas, ovejas y pollos.
 * A todo lo demás que da miedo le tiene miedo: gime, tiembla y huye, y no espanta a nada.
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class LunaMiedo {
    private static final Map<UUID, Integer> avisoCd = new HashMap<>();
    private static int reloj = 0;

    static boolean esLuna(Entity e) {
        return e instanceof Wolf && e.getTags().contains("dv_luna");
    }

    static boolean presa(Entity e) {
        EntityType<?> t = e.getType();
        return t == EntityType.COW || t == EntityType.SHEEP || t == EntityType.CHICKEN;
    }

    static boolean daMiedo(Entity e) {
        if (e == null || !e.isAlive()) return false;
        if (e instanceof Monstruo || e instanceof Masa || e instanceof Marina) return true;
        var t = e.getTags();
        return CanonServidor.esHorror(e) || t.contains("dv_nicolas") || t.contains("dv_sinrostro") || t.contains("dv_miracerca")
                || t.contains("dv_lejos") || t.contains("dv_lbicho") || t.contains("dv_lfalsa") || t.contains("dv_dhum")
                || t.contains("dv_demonio") || t.contains("dv_jefe") || t.contains("dv_fantasma") || t.contains("dv_imitador");
    }

    /** No puede ponerse a pelear con nada que no sea vaca, oveja o pollo. */
    @SubscribeEvent
    public static void objetivo(LivingChangeTargetEvent e) {
        if (!esLuna(e.getEntity())) return;
        LivingEntity t = e.getNewTarget();
        if (t != null && !presa(t)) e.setCanceled(true);
    }

    @SubscribeEvent
    public static void ataque(LivingAttackEvent e) {
        if (esLuna(e.getSource().getEntity()) && !presa(e.getEntity())) e.setCanceled(true);
    }

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent ev) {
        if (ev.phase != TickEvent.Phase.END || ++reloj % 5 != 0) return;
        for (ServerPlayer p : ev.getServer().getPlayerList().getPlayers()) {
            if (!(p.level() instanceof ServerLevel lv)) continue;
            List<Wolf> lunas = lv.getEntitiesOfClass(Wolf.class, p.getBoundingBox().inflate(48), LunaMiedo::esLuna);
            for (Wolf w : lunas) asustar(lv, w);
        }
        avisoCd.replaceAll((k, v) -> v - 5);
        avisoCd.values().removeIf(v -> v <= 0);
    }

    static void asustar(ServerLevel lv, Wolf w) {
        Entity cosa = null;
        double best = 1e9;
        for (Entity e : lv.getEntities(w, w.getBoundingBox().inflate(14), LunaMiedo::daMiedo)) {
            double d = e.distanceToSqr(w);
            if (d < best) { best = d; cosa = e; }
        }
        if (cosa == null) return;
        if (w.getTarget() != null && !presa(w.getTarget())) w.setTarget(null);
        if (w.isAngry() && (w.getTarget() == null || !presa(w.getTarget()))) w.stopBeingAngry();
        // tiembla y gime
        if (reloj % 40 == 0) {
            lv.playSound(null, w.getX(), w.getY(), w.getZ(), SoundEvents.WOLF_WHINE, SoundSource.NEUTRAL, 1.0f, 0.8f + w.getRandom().nextFloat() * 0.3f);
            lv.broadcastEntityEvent(w, (byte) 8); // se sacude temblando
        }
        // huye: corre lejos de eso (aunque esté sentada, se levanta del susto)
        if (!w.isInSittingPose() || best < 25) {
            Vec3 lejos = w.position().subtract(cosa.position());
            if (lejos.lengthSqr() < 0.01) lejos = new Vec3(1, 0, 0);
            Vec3 obj = w.position().add(lejos.normalize().scale(10));
            w.getNavigation().moveTo(obj.x, obj.y, obj.z, 1.6);
        }
        if (reloj % 20 == 0) lv.sendParticles(ParticleTypes.FALLING_WATER, w.getX(), w.getY() + 0.6, w.getZ(), 3, 0.2, 0.2, 0.2, 0);
        if (!avisoCd.containsKey(w.getUUID())) {
            avisoCd.put(w.getUUID(), 600);
            for (ServerPlayer pl : lv.getPlayers(pp -> pp.distanceToSqr(w) < 24 * 24))
                pl.displayClientMessage(net.minecraft.network.chat.Component.literal("Luna gime y tiembla. Le tiene miedo a algo que está cerca.")
                        .withStyle(s -> s.withColor(0xFFD27A).withItalic(true)), true);
        }
    }
}
