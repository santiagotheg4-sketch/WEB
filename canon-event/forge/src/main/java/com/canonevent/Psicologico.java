package com.canonevent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.Score;
import net.minecraft.world.scores.Scoreboard;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Terror psicológico que no se ve venir:
 * - «Fulano se unió a la partida» cuando Fulano NO está jugando, escribe algo raro en el chat y se va.
 * - En las cuevas, unos pasos copian los tuyos... y siguen un poco cuando tú te detienes.
 * - Los objetos de tu barra cambian de lugar solos (de noche, con miedo).
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class Psicologico {
    private static final RandomSource R = RandomSource.create();
    private static int reloj = 0;
    /** visita falsa en curso: nombre, tick en que habla, tick en que se va */
    private static String visitante = null;
    private static int tHabla = -1, tSale = -1;
    private static final Map<UUID, Integer> eco = new HashMap<>();
    private static final Map<UUID, Vec3> ultimo = new HashMap<>();
    private static final Map<UUID, Integer> quietoEco = new HashMap<>();

    static final String[] FRASES = {"hola?", "¿alguien está despierto?", "¿por qué hay alguien en mi casa?", "no me sigan",
            "estoy afuera. ábranme", "¿quién está con ustedes?", "no era yo", "ya los vi", "no me dejen aquí", "¿por qué no me contestan?",
            "hay alguien parado detrás de ti", "no se duerman"};

    /** Se acuerda de todos los que han jugado (para poder fingir que se conectan). */
    @SubscribeEvent
    public static void entra(PlayerEvent.PlayerLoggedInEvent e) {
        if (e.getEntity() instanceof ServerPlayer p) {
            Scoreboard sb = p.getServer().getScoreboard();
            Objective o = sb.getObjective("dv.conocidos");
            if (o == null) o = sb.addObjective("dv.conocidos", net.minecraft.world.scores.criteria.ObjectiveCriteria.DUMMY,
                    Component.literal("conocidos"), net.minecraft.world.scores.criteria.ObjectiveCriteria.RenderType.INTEGER);
            sb.getOrCreatePlayerScore(p.getScoreboardName(), o).setScore(1);
        }
    }

    static int miedo(MinecraftServer s, ServerPlayer p) {
        Scoreboard sb = s.getScoreboard();
        Objective o = sb.getObjective("dv.miedo");
        if (o == null || !sb.hasPlayerScore(p.getScoreboardName(), o)) return 0;
        return sb.getOrCreatePlayerScore(p.getScoreboardName(), o).getScore();
    }

    static int miedoCalma(ServerPlayer p) {
        Scoreboard sb = p.getServer().getScoreboard();
        Objective o = sb.getObjective("dv.calma");
        return (o == null || !sb.hasPlayerScore(p.getScoreboardName(), o)) ? 0 : sb.getOrCreatePlayerScore(p.getScoreboardName(), o).getScore();
    }

    static boolean activo(MinecraftServer s, String clave) {
        Scoreboard sb = s.getScoreboard();
        Objective o = sb.getObjective("dv.cfg");
        return o == null || !sb.hasPlayerScore("#" + clave, o) || sb.getOrCreatePlayerScore("#" + clave, o).getScore() != 0;
    }

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent ev) {
        if (ev.phase != TickEvent.Phase.END) return;
        MinecraftServer s = ev.getServer();
        reloj++;
        // forzar desde comandos: /function canon:admin/psico/visita  y  /function canon:admin/psico/eco
        Scoreboard sb = s.getScoreboard();
        Objective dev = sb.getObjective("dv.dev");
        if (dev != null && reloj % 10 == 0) {
            if (sb.hasPlayerScore("#psico_visita", dev) && sb.getOrCreatePlayerScore("#psico_visita", dev).getScore() == 1) {
                sb.getOrCreatePlayerScore("#psico_visita", dev).setScore(0);
                if (visitante == null) iniciarVisita(s);
            }
            if (sb.hasPlayerScore("#psico_eco", dev) && sb.getOrCreatePlayerScore("#psico_eco", dev).getScore() == 1) {
                sb.getOrCreatePlayerScore("#psico_eco", dev).setScore(0);
                for (ServerPlayer p : s.getPlayerList().getPlayers()) eco.put(p.getUUID(), 600);
            }
        }
        visitaFalsa(s);
        if (reloj % 6 == 0) for (ServerPlayer p : s.getPlayerList().getPlayers()) pasosEco(p);
        if (reloj % 200 == 0 && activo(s, "psico")) for (ServerPlayer p : s.getPlayerList().getPlayers()) barraCambia(s, p);
    }

    // ------------------------------------------------------------ alguien «se conecta»
    static void visitaFalsa(MinecraftServer s) {
        List<ServerPlayer> jugadores = s.getPlayerList().getPlayers();
        if (jugadores.isEmpty()) return;
        if (visitante == null) {
            if (reloj % 1200 != 0 || !activo(s, "psico")) return;
            boolean noche = !jugadores.get(0).level().isDay();
            if (R.nextInt(noche ? 25 : 90) != 0) return;
            iniciarVisita(s);
            return;
        }
        if (reloj == tHabla) {
            Component msg = Component.translatable("chat.type.text", Component.literal(visitante), Component.literal(FRASES[R.nextInt(FRASES.length)]));
            s.getPlayerList().broadcastSystemMessage(msg, false);
            for (ServerPlayer p : jugadores)
                Monstruo.comando(p, "playsound canon:gen.paso_tierra hostile @s ^" + (R.nextInt(7) - 3) + " ^ ^-" + (3 + R.nextInt(4)) + " 0.6 0.9");
        }
        if (reloj >= tSale) {
            s.getPlayerList().broadcastSystemMessage(Component.translatable("multiplayer.player.left", visitante).withStyle(ChatFormatting.YELLOW), false);
            visitante = null;
        }
    }

    /** Elige a alguien que haya jugado antes y que no esté conectado (o a Juan, que ya no está). */
    public static void iniciarVisita(MinecraftServer s) {
        List<String> opciones = new ArrayList<>();
        Scoreboard sb = s.getScoreboard();
        Objective o = sb.getObjective("dv.conocidos");
        if (o != null)
            for (Score sc : sb.getPlayerScores(o)) {
                String n = sc.getOwner();
                if (!n.startsWith("#") && s.getPlayerList().getPlayerByName(n) == null) opciones.add(n);
            }
        visitante = opciones.isEmpty() || R.nextInt(4) == 0 ? "Juan" : opciones.get(R.nextInt(opciones.size()));
        s.getPlayerList().broadcastSystemMessage(Component.translatable("multiplayer.player.joined", visitante).withStyle(ChatFormatting.YELLOW), false);
        tHabla = reloj + 100 + R.nextInt(200);
        tSale = tHabla + 300 + R.nextInt(500);
    }

    // ------------------------------------------------------------ pasos que te copian en las cuevas
    static void pasosEco(ServerPlayer p) {
        if (p.isSpectator() || p.level().canSeeSky(p.blockPosition()) || p.getY() > 55) {
            eco.remove(p.getUUID());
            return;
        }
        UUID id = p.getUUID();
        int t = eco.getOrDefault(id, 0);
        if (t <= 0) {
            if (R.nextInt(1500) == 0 && activo(p.getServer(), "psico") && miedoCalma(p) == 0) eco.put(id, 600); // 30 segundos de eco
            return;
        }
        eco.put(id, t - 6);
        Vec3 ahora = p.position();
        Vec3 antes = ultimo.put(id, ahora);
        boolean camina = antes != null && antes.distanceToSqr(ahora) > 0.04;
        int q = camina ? 0 : quietoEco.getOrDefault(id, 0) + 1;
        quietoEco.put(id, q);
        // copia tus pasos desde atrás... y da uno o dos más cuando te detienes
        if (camina || q == 1 || (q == 2 && R.nextBoolean()))
            Monstruo.comando(p, "playsound canon:gen.paso_tierra hostile @s ^ ^ ^-" + (4 + R.nextInt(3)) + " " + (camina ? 0.45 : 0.6) + " " + (0.8 + R.nextInt(15) / 100.0));
        if (q == 3 && R.nextInt(4) == 0) Monstruo.comando(p, "playsound canon:gen.respira_lenta hostile @s ^ ^ ^-3 0.5 0.9");
    }

    // ------------------------------------------------------------ la barra cambia sola
    static void barraCambia(MinecraftServer s, ServerPlayer p) {
        if (p.isSpectator() || p.isCreative() || p.level().isDay() || miedo(s, p) < 40 || R.nextInt(60) != 0) return;
        var inv = p.getInventory();
        int a = R.nextInt(9), b = R.nextInt(9);
        if (a == b || a == inv.selected || b == inv.selected) return;
        ItemStack x = inv.getItem(a);
        inv.setItem(a, inv.getItem(b));
        inv.setItem(b, x);
    }
}
