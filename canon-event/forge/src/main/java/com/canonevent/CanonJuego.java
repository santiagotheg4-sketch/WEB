package com.canonevent;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.StringArgumentType;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.HoverEvent;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.Style;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.entity.player.PlayerSleepInBedEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Comando /canon, dormir aunque haya personajes del mod cerca, y reconocer a Mari por su nombre. */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID)
public class CanonJuego {

    /** clave -> {comando, descripción}. Lo genera tools/build.py en canon_comandos.txt. */
    static Map<String, String[]> comandos() {
        Map<String, String[]> m = new LinkedHashMap<>();
        try (InputStream in = CanonJuego.class.getResourceAsStream("/canon_comandos.txt")) {
            if (in == null) return m;
            BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8));
            String l;
            while ((l = r.readLine()) != null) {
                String[] p = l.split("\\|", 3);
                if (p.length == 3) m.put(p[0], new String[]{p[1], p[2]});
            }
        } catch (Exception ignored) {
        }
        return m;
    }

    @SubscribeEvent
    public static void registrar(RegisterCommandsEvent e) {
        CommandDispatcher<CommandSourceStack> d = e.getDispatcher();
        d.register(Commands.literal("canon").requires(s -> s.hasPermission(2))
                .executes(c -> ayuda(c.getSource(), ""))
                .then(Commands.literal("lista").executes(c -> ayuda(c.getSource(), ""))
                        .then(Commands.argument("filtro", StringArgumentType.word()).executes(c -> ayuda(c.getSource(), StringArgumentType.getString(c, "filtro")))))
                .then(Commands.argument("accion", StringArgumentType.word())
                        .suggests((c, b) -> SharedSuggestionProvider.suggest(comandos().keySet(), b))
                        .executes(c -> correr(c.getSource(), StringArgumentType.getString(c, "accion")))));
    }

    private static int ayuda(CommandSourceStack s, String filtro) {
        Map<String, String[]> m = comandos();
        s.sendSuccess(() -> Component.literal("\n☾ CANON EVENT — escribe /canon <nombre> o haz clic:").withStyle(ChatFormatting.LIGHT_PURPLE), false);
        int n = 0;
        for (Map.Entry<String, String[]> en : m.entrySet()) {
            String k = en.getKey();
            if (!filtro.isEmpty() && !k.contains(filtro.toLowerCase(Locale.ROOT)) && !en.getValue()[1].toLowerCase(Locale.ROOT).contains(filtro.toLowerCase(Locale.ROOT))) continue;
            MutableComponent line = Component.literal(" [" + k + "] ").withStyle(Style.EMPTY.withColor(ChatFormatting.GOLD)
                            .withClickEvent(new ClickEvent(ClickEvent.Action.RUN_COMMAND, "/canon " + k))
                            .withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, Component.literal("/" + en.getValue()[0]))))
                    .append(Component.literal(en.getValue()[1]).withStyle(ChatFormatting.GRAY));
            s.sendSuccess(() -> line, false);
            n++;
        }
        int total = n;
        s.sendSuccess(() -> Component.literal(total + " acciones. Filtra con /canon lista <palabra> (por ejemplo: /canon lista diana).").withStyle(ChatFormatting.DARK_GRAY), false);
        return n;
    }

    private static int correr(CommandSourceStack s, String clave) {
        String[] c = comandos().get(clave);
        if (c == null) {
            s.sendFailure(Component.literal("No existe «" + clave + "». Escribe /canon lista"));
            return 0;
        }
        s.getServer().getCommands().performPrefixedCommand(s, c[0]);
        return 1;
    }

    // ------------------------------------------------------------------ dormir
    /** Los personajes del mod usan un zombi invisible por dentro: Minecraft creía que había monstruos y no dejaba dormir. */
    @SubscribeEvent
    public static void dormir(PlayerSleepInBedEvent e) {
        if (!(e.getEntity() instanceof ServerPlayer p) || e.getResultStatus() != null) return;
        BlockPos pos = e.getPos();
        ServerLevel lvl = p.serverLevel();
        if (lvl.isDay() || !lvl.dimensionType().natural()) return;
        if (!p.position().closerThan(Vec3.atBottomCenterOf(pos), 3.0)) return;
        Vec3 c = Vec3.atBottomCenterOf(pos);
        List<Monster> cerca = lvl.getEntitiesOfClass(Monster.class, new AABB(c.x - 8, c.y - 5, c.z - 8, c.x + 8, c.y + 5, c.z + 8),
                m -> m.isPreventingPlayerRest(p));
        if (cerca.isEmpty()) return;
        boolean real = cerca.stream().anyMatch(m -> !m.getTags().contains("dv_brain"));
        if (real) return; // hay monstruos de verdad: Minecraft decide
        p.setRespawnPosition(lvl.dimension(), pos, p.getYRot(), false, true);
        p.startSleeping(pos);
        lvl.updateSleepingPlayerList();
        e.setResult(Player.BedSleepingProblem.OTHER_PROBLEM); // ya está durmiendo; esto solo evita el chequeo de monstruos
    }

    // ------------------------------------------------------------------ Mari
    @SubscribeEvent
    public static void entra(PlayerEvent.PlayerLoggedInEvent e) {
        String n = e.getEntity().getGameProfile().getName().toLowerCase(Locale.ROOT);
        if (n.contains("mari") && !n.contains("mariana")) e.getEntity().addTag("dv_mari");
    }
}
