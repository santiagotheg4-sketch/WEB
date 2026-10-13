package com.canonevent;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.resources.sounds.AbstractTickableSoundInstance;
import net.minecraft.client.resources.sounds.SoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.CustomizeGuiOverlayEvent;
import net.minecraftforge.client.event.RegisterGuiOverlaysEvent;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Lado del jugador: medidor de miedo junto a la barra de ítems, aviso de acecho, música de persecución y ambiente. */
public class CanonCliente {
    static int miedo = 0;
    static float miedoVisto = 0;
    static String acechador = "";
    static boolean visto = false, persecucion = false;
    static float distancia = -1;
    /** ticks de temblor de pantalla (solo visual: no mueve tu mira) */
    static int temblor = 0;
    static Bucle musica, viento, zumbido, tension;
    /** estática en la pantalla (ticks) y ojos en la oscuridad (ticks, posición) */
    static int glitch = 0, ojos = 0, ojosX = 0, ojosY = 0;
    static final java.util.Random AZAR = new java.util.Random();

    static void recibir(CanonRed.Estado e) {
        miedo = e.miedo();
        acechador = e.acechador();
        visto = e.visto();
        persecucion = e.persecucion();
        distancia = e.distancia();
        temblor = Math.max(temblor, e.temblor());
    }

    /** Sonido en bucle con volumen que sube y baja suave. */
    static class Bucle extends AbstractTickableSoundInstance {
        float objetivo = 0f;
        final float vel;

        Bucle(String id, float vel) {
            super(SoundEvent.createVariableRangeEvent(new ResourceLocation("canon", id)), SoundSource.AMBIENT, SoundInstance.createUnseededRandom());
            this.looping = true;
            this.delay = 0;
            this.volume = 0.001f;
            this.relative = true;
            this.attenuation = SoundInstance.Attenuation.NONE;
            this.vel = vel;
        }

        @Override
        public void tick() {
            volume += Mth.clamp(objetivo - volume, -vel, vel);
            if (objetivo <= 0 && volume <= 0.002f) stop();
        }

        boolean vivo() {
            return !isStopped() && Minecraft.getInstance().getSoundManager().isActive(this);
        }
    }

    static Bucle asegurar(Bucle b, String id, float vel, float objetivo) {
        if (objetivo > 0 && (b == null || !b.vivo())) {
            b = new Bucle(id, vel);
            Minecraft.getInstance().getSoundManager().play(b);
        }
        if (b != null) b.objetivo = objetivo;
        return b;
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT)
    public static class Juego {
        @SubscribeEvent
        public static void tick(TickEvent.ClientTickEvent e) {
            Minecraft mc = Minecraft.getInstance();
            if (e.phase != TickEvent.Phase.END || mc.player == null || mc.level == null) return;
            miedoVisto += (miedo - miedoVisto) * 0.1f;
            boolean noche = !mc.level.isDay();
            boolean afuera = mc.level.canSeeSky(mc.player.blockPosition());
            musica = asegurar(musica, "gen.persecucion", 0.03f, persecucion ? 1.0f : 0f);
            if (persecucion) mc.getMusicManager().stopPlaying();
            viento = asegurar(viento, "gen.viento", 0.01f, (noche && afuera && !persecucion) ? 0.35f : 0f);
            // música de tensión con eco: sube despacio cuando algo te acecha (no te persigue todavía)
            float tObj = persecucion ? 0f : !acechador.isEmpty() ? (visto ? 0.6f : 0.45f) : miedo >= 50 ? 0.2f : 0f;
            tension = asegurar(tension, "gen.tension", 0.004f, tObj);
            zumbido = asegurar(zumbido, "gen.drone", 0.01f, (!persecucion && miedo >= 35) ? Math.min(0.6f, (miedo - 30) / 80f) : 0f);
            // con mucho miedo la pantalla se llena de estática un instante
            if (temblor > 0) temblor--;
            if (glitch > 0) glitch--;
            else if (miedo >= 75 && AZAR.nextInt(miedo >= 90 ? 400 : 900) == 0) {
                glitch = 4 + AZAR.nextInt(5);
                mc.getSoundManager().play(net.minecraft.client.resources.sounds.SimpleSoundInstance.forUI(
                        SoundEvent.createVariableRangeEvent(new ResourceLocation("canon", "gen.estatica")), 1.0f, 0.6f));
            }
            // en la oscuridad total, a veces hay dos ojos rojos mirándote desde un borde
            if (ojos > 0) ojos--;
            else if (miedo >= 30 && mc.level.getMaxLocalRawBrightness(mc.player.blockPosition().above()) <= 2 && AZAR.nextInt(1200) == 0) {
                ojos = 40 + AZAR.nextInt(40);
                int w = mc.getWindow().getGuiScaledWidth(), h = mc.getWindow().getGuiScaledHeight();
                boolean izq = AZAR.nextBoolean();
                ojosX = izq ? 10 + AZAR.nextInt(w / 6) : w - 30 - AZAR.nextInt(w / 6);
                ojosY = 20 + AZAR.nextInt(Math.max(1, h / 2));
            }
        }

        /** La cámara tiembla cuando algo te persigue y está cerca (más cerca, más tiembla). */
        @SubscribeEvent
        public static void camara(net.minecraftforge.client.event.ViewportEvent.ComputeCameraAngles e) {
            Minecraft mc = Minecraft.getInstance();
            if (mc.player == null || mc.level == null || mc.options.getCameraType() != net.minecraft.client.CameraType.FIRST_PERSON) return;
            float f = 0f;
            if (persecucion && distancia >= 0 && distancia < 12) f = (12 - distancia) / 12f;
            if (miedoVisto >= 85) f = Math.max(f, (miedoVisto - 85) / 60f);
            if (temblor > 0) f = Math.max(f, Math.min(1.6f, temblor / 15f));
            if (f <= 0.01f) return;
            double t = mc.level.getGameTime() + e.getPartialTick();
            e.setRoll((float) (e.getRoll() + Math.sin(t * 1.7) * 1.6 * f));
            e.setPitch((float) (e.getPitch() + Math.sin(t * 2.3 + 1) * 0.9 * f));
            e.setYaw((float) (e.getYaw() + Math.cos(t * 1.9) * 0.7 * f));
        }

        /** La barra de miedo vieja (arriba) se esconde: ahora va abajo. */
        @SubscribeEvent
        public static void barraVieja(CustomizeGuiOverlayEvent.BossEventProgress e) {
            String n = e.getBossEvent().getName().getString();
            if (n.contains("MIEDO") || n.startsWith("Miedo")) {
                e.setCanceled(true);
                e.setIncrement(0);
            }
        }
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistroCliente {
        @SubscribeEvent
        public static void overlays(RegisterGuiOverlaysEvent e) {
            e.registerAbove(VanillaGuiOverlay.HOTBAR.id(), "miedo", (gui, g, pt, w, h) -> dibujar(g, w, h));
        }
    }

    static final String[] ESTADO = {"tranquilo", "inquieto", "asustado", "aterrado", "ya no estás solo"};
    static final int[] COLOR = {0xFFE8E8E8, 0xFFE8E0A0, 0xFFFFE15A, 0xFFFFA040, 0xFFFF3030};

    static void dibujar(GuiGraphics g, int w, int h) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player == null || mc.options.hideGui || mc.player.isSpectator()) return;
        int m = Math.round(miedoVisto);
        int k = m < 20 ? 0 : m < 40 ? 1 : m < 60 ? 2 : m < 80 ? 3 : 4;
        // medidor: a la derecha de la barra de ítems
        int x = w / 2 + 98, y = h - 21;
        int tiembla = (k >= 3 && mc.level != null && mc.level.getGameTime() % 4 < 2) ? 1 : 0;
        g.fill(x - 2, y - 2, x + 86, y + 20, 0x88000000);
        g.blit(new ResourceLocation("canon", "textures/font/miedo" + k + ".png"), x + tiembla, y, 0, 0, 16, 16, 16, 16);
        g.drawString(mc.font, "MIEDO", x + 19, y, 0xFFB0B0B0, true);
        g.drawString(mc.font, m + "%", x + 19, y + 9, COLOR[k], true);
        int barra = Math.round(42 * m / 100f);
        g.fill(x + 19 + 22, y + 11, x + 19 + 22 + 42, y + 14, 0xFF301010);
        g.fill(x + 19 + 22, y + 11, x + 19 + 22 + barra, y + 14, COLOR[k]);
        // aviso de acecho, encima de los corazones
        if (!acechador.isEmpty()) {
            long tt = mc.level == null ? 0 : mc.level.getGameTime();
            String msg = visto ? "◉ " + (acechador.equals("Algo") ? "Algo" : acechador) + " te está mirando" : "Sientes que te acechan...";
            if (persecucion) msg = "¡" + (acechador.equals("Algo") ? "Algo" : acechador) + " te está persiguiendo!";
            int alpha = (int) (160 + 95 * Math.sin(tt * 0.3));
            int col = persecucion ? 0xFF2020 : visto ? 0xFF6060 : 0xC8A0A0;
            int tw = mc.font.width(msg);
            g.drawString(mc.font, msg, w / 2 - tw / 2, h - 59 - (mc.player.getArmorValue() > 0 ? 10 : 0), (alpha << 24) | col, true);
        }
        // ojos en la oscuridad (parpadean)
        if (ojos > 0 && !(ojos % 23 < 2)) {
            int a = Math.min(255, ojos * 8);
            int c = (a << 24) | 0xC01010;
            g.fill(ojosX, ojosY, ojosX + 2, ojosY + 1, c);
            g.fill(ojosX + 6, ojosY, ojosX + 8, ojosY + 1, c);
        }
        // estática
        if (glitch > 0) {
            for (int i = 0; i < 700; i++) {
                int px = AZAR.nextInt(w), py = AZAR.nextInt(h), v = AZAR.nextInt(255);
                g.fill(px, py, px + 2, py + 2, 0xB0000000 | (v << 16) | (v << 8) | v);
            }
            for (int i = 0; i < 4; i++) {
                int ly = AZAR.nextInt(h);
                g.fill(0, ly, w, ly + 1 + AZAR.nextInt(3), 0x60FFFFFF);
            }
        }
        // viñeta roja suave cuando el miedo es muy alto
        if (m >= 70) {
            int a = (int) ((m - 70) / 30f * 90);
            g.fillGradient(0, 0, w, h / 5, (a << 24) | 0x400000, 0x00000000);
            g.fillGradient(0, h - h / 5, w, h, 0x00000000, (a << 24) | 0x400000);
        }
    }
}
