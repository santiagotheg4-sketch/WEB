package com.canonevent;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.vehicle.Boat;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.Scoreboard;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Cuándo y dónde salen las criaturas del agua: cerca de ríos, lagos y el mar (más de noche).
 * La Ahogada se asoma lejos, donde la puedas ver; si vas en bote o nadando, a veces está en la orilla mirándote.
 * El Leviatán solo cuando estás en agua honda.
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class Mar {
    private static int reloj = 0;
    private static final RandomSource R = RandomSource.create();

    static boolean activo(ServerLevel lv) {
        Scoreboard sb = lv.getServer().getScoreboard();
        Objective o = sb.getObjective("dv.cfg");
        return o == null || !sb.hasPlayerScore("#mar", o) || sb.getOrCreatePlayerScore("#mar", o).getScore() != 0;
    }

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent ev) {
        if (ev.phase != TickEvent.Phase.END || ++reloj % 20 != 0) return;
        for (ServerPlayer p : ev.getServer().getPlayerList().getPlayers()) {
            if (p.isSpectator() || p.isCreative() || !(p.level() instanceof ServerLevel lv) || lv.dimension() != Level.OVERWORLD) continue;
            if (!activo(lv)) return;
            if (NicolasMina.puntaje(lv, p.getScoreboardName(), "dv.calma", 0) > 0) continue; // calma después de un susto
            boolean noche = !lv.isDay();
            boolean enAgua = p.isInWater() || p.getVehicle() instanceof Boat;
            if (lv.getEntitiesOfClass(Marina.class, p.getBoundingBox().inflate(96), m -> m.tipo == Marina.Tipo.AHOGADA).isEmpty()) {
                int chance = noche ? 70 : 260;
                if (enAgua) chance /= 2;
                if (R.nextInt(chance) == 0) ahogada(lv, p, enAgua && R.nextBoolean());
            }
            if (enAgua && lv.getEntitiesOfClass(Marina.class, p.getBoundingBox().inflate(160), m -> m.tipo == Marina.Tipo.LEVIATAN).isEmpty()
                    && profundidad(lv, p.blockPosition()) >= 8 && R.nextInt(noche ? 120 : 500) == 0)
                leviatan(lv, p);
        }
    }

    static int profundidad(ServerLevel lv, BlockPos b) {
        int n = 0;
        BlockPos q = b;
        while (n < 40 && (lv.getFluidState(q).is(FluidTags.WATER) || lv.getBlockState(q).isAir())) {
            if (lv.getFluidState(q).is(FluidTags.WATER)) n++;
            q = q.below();
        }
        return n;
    }

    static boolean seVe(ServerLevel lv, ServerPlayer p, Vec3 punto) {
        HitResult h = lv.clip(new ClipContext(p.getEyePosition(), punto, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
        return h.getType() == HitResult.Type.MISS || h.getLocation().distanceTo(punto) < 1.5;
    }

    /** Busca agua (o una orilla) lejos de ti pero a la vista, y la pone ahí. */
    public static boolean ahogada(ServerLevel lv, ServerPlayer p, boolean orilla) {
        for (int intento = 0; intento < 30; intento++) {
            double a = R.nextDouble() * Math.PI * 2, r = 14 + R.nextDouble() * 20;
            int x = (int) Math.floor(p.getX() + Math.cos(a) * r), z = (int) Math.floor(p.getZ() + Math.sin(a) * r);
            for (int y = (int) p.getY() + 8; y > (int) p.getY() - 12; y--) {
                BlockPos b = new BlockPos(x, y, z);
                if (!orilla && lv.getFluidState(b).is(FluidTags.WATER) && lv.getBlockState(b.above()).isAir()) {
                    if (!lv.getFluidState(b.below()).is(FluidTags.WATER) || !lv.getFluidState(b.below(2)).is(FluidTags.WATER)) break;
                    Vec3 pos = new Vec3(x + 0.5, y + 1.2, z + 0.5);
                    if (!seVe(lv, p, pos)) break;
                    return poner(lv, p, x + 0.5, y - 0.4, z + 0.5, false);
                }
                if (orilla && lv.getBlockState(b).isSolid() && lv.getBlockState(b.above()).isAir() && lv.getBlockState(b.above(2)).isAir()) {
                    boolean agua = false;
                    for (int dx = -2; dx <= 2 && !agua; dx++)
                        for (int dz = -2; dz <= 2 && !agua; dz++)
                            agua = lv.getFluidState(b.offset(dx, 0, dz)).is(FluidTags.WATER);
                    if (!agua || !seVe(lv, p, new Vec3(x + 0.5, y + 2.5, z + 0.5))) break;
                    return poner(lv, p, x + 0.5, y + 1, z + 0.5, true);
                }
                if (lv.getBlockState(b).isSolid()) break;
            }
        }
        return false;
    }

    static boolean poner(ServerLevel lv, ServerPlayer p, double x, double y, double z, boolean orilla) {
        Marina m = CanonEntidades.AHOGADA.get().create(lv);
        if (m == null) return false;
        m.moveTo(x, y, z, R.nextFloat() * 360f, 0);
        if (orilla) m.enOrilla();
        m.finalizeSpawn(lv, lv.getCurrentDifficultyAt(m.blockPosition()), MobSpawnType.EVENT, null, null);
        lv.addFreshEntity(m);
        return true;
    }

    public static boolean leviatan(ServerLevel lv, ServerPlayer p) {
        for (int intento = 0; intento < 12; intento++) {
            double a = R.nextDouble() * Math.PI * 2;
            BlockPos b = BlockPos.containing(p.getX() + Math.cos(a) * 26, p.getY() - 8, p.getZ() + Math.sin(a) * 26);
            if (!lv.getFluidState(b).is(FluidTags.WATER)) continue;
            Marina m = CanonEntidades.LEVIATAN.get().create(lv);
            if (m == null) return false;
            m.moveTo(b.getX() + 0.5, b.getY(), b.getZ() + 0.5, 0, 0);
            lv.addFreshEntity(m);
            Monstruo.comando(p, "playsound canon:mar.gemido hostile @s ~ ~-10 ~ 1 0.5");
            Monstruo.comando(p, "title @s actionbar {\"text\":\"Algo grande se mueve debajo de ti\",\"color\":\"#5f8fa8\",\"italic\":true}");
            return true;
        }
        return false;
    }
}
