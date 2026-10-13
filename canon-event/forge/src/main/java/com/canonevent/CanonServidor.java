package com.canonevent;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.Scoreboard;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.network.PacketDistributor;

/** Cada medio segundo: miedo, acechadores a la vista, persecuciones y pasos cuando te quedas quieto. */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class CanonServidor {
    private static int reloj = 0;
    private static final Map<UUID, Double> distAnterior = new HashMap<>();
    private static final Map<UUID, Integer> persigue = new HashMap<>();
    private static final Map<UUID, Vec3> posAnterior = new HashMap<>();
    private static final Map<UUID, Integer> quieto = new HashMap<>();
    private static final RandomSource R = RandomSource.create();

    static boolean esHorror(Entity e) {
        var t = e.getTags();
        return (t.contains("dv_horror") || t.contains("dv_asomo") || t.contains("dv_zunga") || t.contains("dv_diana")
                || t.contains("dv_alto") || t.contains("dv_miron")) && !t.contains("dv_luna");
    }

    static String nombre(Entity e) {
        String n = e.hasCustomName() ? e.getCustomName().getString() : "";
        return (n.isBlank() || n.contains("?")) ? "Algo" : n;
    }

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent ev) {
        if (ev.phase != TickEvent.Phase.END) return;
        if (++reloj % 10 != 0) return;
        MinecraftServer srv = ev.getServer();
        Scoreboard sb = srv.getScoreboard();
        Objective miedoObj = sb.getObjective("dv.miedo");
        for (ServerPlayer p : srv.getPlayerList().getPlayers()) {
            int miedo = 0;
            String nom = p.getScoreboardName();
            if (miedoObj != null && sb.hasPlayerScore(nom, miedoObj)) miedo = Math.max(0, Math.min(100, sb.getOrCreatePlayerScore(nom, miedoObj).getScore()));

            // ¿quién me acecha?
            List<Entity> cerca = p.level().getEntities((Entity) null, p.getBoundingBox().inflate(40), CanonServidor::esHorror);
            Entity mejor = null;
            double dmin = 1e9;
            boolean visto = false;
            for (Entity e : cerca) {
                double d = e.distanceTo(p);
                boolean vis = p.hasLineOfSight(e);
                if ((vis && !visto) || (vis == visto && d < dmin)) {
                    mejor = e; dmin = d; visto = vis;
                }
            }
            String acecha = "";
            boolean persecucion = false;
            if (mejor != null && (visto || dmin < 20)) {
                acecha = nombre(mejor);
                Double antes = distAnterior.get(mejor.getUUID());
                int racha = persigue.getOrDefault(p.getUUID(), 0);
                if (antes != null && dmin < 22 && antes - dmin > 0.35) racha = Math.min(racha + 1, 8);
                else racha = Math.max(racha - 1, 0);
                persigue.put(p.getUUID(), racha);
                persecucion = racha >= 2;
                distAnterior.put(mejor.getUUID(), dmin);
            } else {
                persigue.put(p.getUUID(), Math.max(persigue.getOrDefault(p.getUUID(), 0) - 1, 0));
                persecucion = persigue.get(p.getUUID()) >= 2;
            }
            Objective shakeObj = sb.getObjective("dv.shake");
            int temblor = (shakeObj != null && sb.hasPlayerScore(nom, shakeObj)) ? Math.max(0, sb.getOrCreatePlayerScore(nom, shakeObj).getScore()) : 0;
            CanonRed.CANAL.send(PacketDistributor.PLAYER.with(() -> p),
                    new CanonRed.Estado(miedo, acecha, visto, persecucion, mejor == null ? -1f : (float) dmin, temblor));

            // pasos que solo se oyen cuando te quedas quieto (de noche, o con miedo)
            Vec3 ahora = p.position();
            Vec3 ant = posAnterior.put(p.getUUID(), ahora);
            int q = (ant != null && ant.distanceToSqr(ahora) < 0.01) ? quieto.getOrDefault(p.getUUID(), 0) + 1 : 0;
            quieto.put(p.getUUID(), q);
            boolean noche = !p.level().isDay();
            if (q >= 10 && (noche || miedo >= 40) && !p.isSpectator() && R.nextInt(18) == 0) {
                String son = p.level().canSeeSky(p.blockPosition()) ? "canon:gen.paso_tierra" : "canon:gen.paso_madera";
                comando(p, "playsound " + son + " hostile @s ^" + (R.nextInt(5) - 2) + " ^ ^-" + (2 + R.nextInt(3)) + " 0.7 " + (0.85 + R.nextInt(30) / 100.0));
                if (R.nextInt(4) == 0)
                    comando(p, "playsound canon:gen.paso_madera hostile @s ^ ^ ^-2 0.6 0.9");
            }
        }
    }

    static void comando(ServerPlayer p, String cmd) {
        p.getServer().getCommands().performPrefixedCommand(p.createCommandSourceStack().withSuppressedOutput().withPermission(4), cmd);
    }
}
