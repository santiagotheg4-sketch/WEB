package com.canonevent;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.Mth;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.Scoreboard;
import net.minecraftforge.event.level.BlockEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Estás picando piedra en una cueva y, de la nada, al romper un bloque, Nicolás está del otro lado:
 * agarrado de los bordes del hueco con las dos manos, con los ojos blancos, mirándote.
 * Pasa muy pocas veces (y nunca dos veces seguidas en poco tiempo), para que te agarre desprevenido.
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class NicolasMina {
    private static final RandomSource R = RandomSource.create();
    private static final Map<UUID, Long> ultima = new HashMap<>();

    static int puntaje(ServerLevel lv, String quien, String obj, int def) {
        Scoreboard sb = lv.getServer().getScoreboard();
        Objective o = sb.getObjective(obj);
        return (o == null || !sb.hasPlayerScore(quien, o)) ? def : sb.getOrCreatePlayerScore(quien, o).getScore();
    }

    @SubscribeEvent
    public static void rompe(BlockEvent.BreakEvent e) {
        if (!(e.getPlayer() instanceof ServerPlayer p) || p.isCreative() || p.isSpectator() || !(p.level() instanceof ServerLevel lv)) return;
        BlockState st = e.getState();
        BlockPos pos = e.getPos();
        if (!st.is(BlockTags.BASE_STONE_OVERWORLD) && !st.is(BlockTags.STONE_ORE_REPLACEABLES) && !st.is(BlockTags.DEEPSLATE_ORE_REPLACEABLES)) return;
        if (lv.canSeeSky(pos) || p.getY() > 50) return;
        if (puntaje(lv, "#nicolas", "dv.cfg", 1) != 1 || puntaje(lv, p.getScoreboardName(), "dv.calma", 0) > 0) return;
        long ahora = lv.getGameTime();
        if (ahora - ultima.getOrDefault(p.getUUID(), -99999L) < 20 * 60 * 15) return; // máximo una vez cada 15 minutos
        if (R.nextInt(200) != 0) return;
        // el bloque tiene que estar a la altura de tu cara o de tu pecho
        int dy = pos.getY() - p.blockPosition().getY();
        if (dy < 0 || dy > 1) return;
        if (!lv.getEntitiesOfClass(Nicolas.class, p.getBoundingBox().inflate(64)).isEmpty()) return;
        Vec3 dir = Vec3.atCenterOf(pos).subtract(p.getEyePosition());
        Direction d = Math.abs(dir.x) > Math.abs(dir.z) ? (dir.x > 0 ? Direction.EAST : Direction.WEST) : (dir.z > 0 ? Direction.SOUTH : Direction.NORTH);
        BlockPos atras = pos.relative(d);
        Nicolas n = CanonEntidades.NICOLAS.get().create(lv);
        if (n == null) return;
        double x = atras.getX() + 0.5 - d.getStepX() * 0.62, z = atras.getZ() + 0.5 - d.getStepZ() * 0.62; // la cara llena el hueco
        double y = pos.getY() + 0.5 - 1.5;
        float yaw = (float) (Mth.atan2(p.getZ() - z, p.getX() - x) * Mth.RAD_TO_DEG) - 90f;
        n.moveTo(x, y, z, yaw, 0);
        n.setYHeadRot(yaw);
        n.setYBodyRot(yaw);
        n.addTag("dv_nagarra");
        lv.addFreshEntity(n);
        ultima.put(p.getUUID(), ahora);
    }
}
