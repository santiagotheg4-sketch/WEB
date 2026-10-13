package com.canonevent;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Kevin corre detrás de ti por las catacumbas: sigue tu rastro paso a paso (por donde tú pasaste),
 * así nunca atraviesa paredes. Si se queda atrás, corre más rápido; si está pegado a ti, espera.
 * Funciona con cualquier personaje del datapack que tenga la etiqueta dv_rastro.
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class Rastro {
    private static final Map<UUID, ArrayDeque<Vec3>> rastros = new HashMap<>();

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent ev) {
        if (ev.phase != TickEvent.Phase.END) return;
        MinecraftServer srv = ev.getServer();
        List<ServerPlayer> part = new ArrayList<>();
        for (ServerPlayer p : srv.getPlayerList().getPlayers())
            if (p.getTags().contains("dv_kpart") && !p.isSpectator()) part.add(p);
        if (part.isEmpty()) {
            rastros.clear();
            return;
        }
        for (ServerPlayer p : part) {
            ArrayDeque<Vec3> r = rastros.computeIfAbsent(p.getUUID(), k -> new ArrayDeque<>());
            Vec3 pos = p.position();
            if (!p.onGround() && !r.isEmpty()) continue; // en el aire no: Kevin no flota
            if (r.isEmpty() || r.peekLast().distanceToSqr(pos) > 0.16) r.addLast(pos);
            if (r.peekLast().distanceToSqr(pos) > 64) { r.clear(); r.addLast(pos); } // se teletransportó
            while (r.size() > 600) r.removeFirst();
        }
        for (ServerLevel lv : srv.getAllLevels()) {
            for (Entity e : lv.getEntities().getAll()) {
                if (!(e instanceof Zombie) || !e.getTags().contains("dv_rastro")) continue;
                ServerPlayer obj = null;
                double best = 1e9;
                for (ServerPlayer p : part) {
                    if (p.level() != lv) continue;
                    double d = p.distanceToSqr(e);
                    if (d < best) { best = d; obj = p; }
                }
                if (obj != null) seguir(e, obj, rastros.get(obj.getUUID()));
            }
        }
    }

    /** Un punto del rastro de ese jugador, unos bloques de camino detrás de él (o null). */
    static Vec3 detrasDe(UUID jugador, double bloques) {
        ArrayDeque<Vec3> r = rastros.get(jugador);
        if (r == null || r.size() < 2) return null;
        Vec3[] pts = r.toArray(new Vec3[0]);
        double atras = 0;
        int j = pts.length - 1;
        while (j > 0 && atras < bloques) { atras += pts[j].distanceTo(pts[j - 1]); j--; }
        return atras >= bloques * 0.6 ? pts[j] : null;
    }

    static void seguir(Entity k, ServerPlayer p, ArrayDeque<Vec3> rastro) {
        if (rastro == null || rastro.isEmpty()) return;
        Vec3[] pts = rastro.toArray(new Vec3[0]);
        Vec3 yo = k.position();
        // el punto del rastro más cercano a Kevin (preferimos los más nuevos)
        int idx = -1;
        double dmin = 1e9;
        for (int i = pts.length - 1; i >= 0; i--) {
            double d = pts[i].distanceToSqr(yo);
            if (d < dmin - 0.01) { dmin = d; idx = i; }
        }
        // cuánto camino le falta hasta ti
        double falta = 0;
        for (int i = idx; i < pts.length - 1; i++) falta += pts[i].distanceTo(pts[i + 1]);
        falta += pts[pts.length - 1].distanceTo(p.position());
        if (dmin > 9 || falta > 45) {
            // se perdió o quedó muy atrás: aparece en tu rastro, unos pasos detrás de ti
            double atras = 0;
            int j = pts.length - 1;
            while (j > 0 && atras < 6) { atras += pts[j].distanceTo(pts[j - 1]); j--; }
            Vec3 a = pts[j];
            k.teleportTo(a.x, a.y, a.z);
            return;
        }
        if (falta < 2.8) {
            // pegado a ti: te mira
            Vec3 dir = p.position().subtract(yo);
            float yaw = (float) (Mth.atan2(dir.z, dir.x) * Mth.RAD_TO_DEG) - 90f;
            girar(k, yaw);
            return;
        }
        double vel = falta > 10 ? 0.4 : falta > 5 ? 0.33 : 0.24;
        Vec3 pos = yo;
        int i = idx;
        double queda = vel;
        Vec3 dirFinal = null;
        while (queda > 0 && i < pts.length) {
            Vec3 meta = (i + 1 < pts.length) ? pts[i + 1] : p.position();
            Vec3 d = meta.subtract(pos);
            double len = d.length();
            if (len < 1e-4) { i++; continue; }
            if (len <= queda) { pos = meta; queda -= len; i++; dirFinal = d; }
            else { pos = pos.add(d.scale(queda / len)); dirFinal = d; queda = 0; }
            if (i + 1 >= pts.length) break;
        }
        if (dirFinal == null) return;
        float yaw = (float) (Mth.atan2(dirFinal.z, dirFinal.x) * Mth.RAD_TO_DEG) - 90f;
        k.teleportTo(pos.x, pos.y, pos.z);
        girar(k, yaw);
    }

    static void girar(Entity k, float yaw) {
        float y = Mth.rotLerp(0.35f, k.getYRot(), yaw);
        k.setYRot(y);
        k.setYHeadRot(y);
        if (k instanceof Zombie z) z.setYBodyRot(y);
    }
}
