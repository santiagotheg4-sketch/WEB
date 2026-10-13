package com.canonevent;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import com.mojang.math.Transformation;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Display;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RenderLivingEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Personajes con skin dibujados como jugadores de verdad (modelo 3D de jugador con su skin, caminar suave,
 * respiración, poses y caras). Los personajes siguen siendo «cerebros» invisibles del datapack con piezas encima;
 * aquí leemos qué pieza tienen puesta (número de modelo) para saber quién son, en qué pose están y qué cara tienen.
 */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT)
public class PersonaRender {
    record Pieza(String quien, String que) {}

    private static Map<Integer, Pieza> cuerpos, caras;
    private static PlayerModel<LivingEntity> modelo, modeloFino;
    record Skin(ResourceLocation tex, boolean fino) {}
    /** brain id -> skin del jugador que copia el doble */
    private static final Map<Integer, Skin> dobles = new HashMap<>();

    /** Lee la cabeza de jugador que lleva el doble y busca la skin de ese jugador (si está conectado, la de su perfil). */
    static Skin skinDe(LivingEntity ent) {
        for (Entity p : ent.getPassengers()) {
            if (!(p instanceof Display.ItemDisplay d) || d.itemRenderState() == null) continue;
            ItemStack it = d.itemRenderState().itemStack();
            if (!it.is(Items.PLAYER_HEAD)) continue;
            CompoundTag t = it.getTag();
            com.mojang.authlib.GameProfile gp = null;
            if (t != null && t.contains("SkullOwner", 10)) gp = net.minecraft.nbt.NbtUtils.readGameProfile(t.getCompound("SkullOwner"));
            else if (t != null && t.contains("SkullOwner", 8)) gp = new com.mojang.authlib.GameProfile(null, t.getString("SkullOwner"));
            Minecraft mc = Minecraft.getInstance();
            if (gp != null && gp.getName() != null && mc.getConnection() != null) {
                net.minecraft.client.multiplayer.PlayerInfo info = mc.getConnection().getPlayerInfo(gp.getName());
                if (info != null) return new Skin(info.getSkinLocation(), "slim".equals(info.getModelName()));
            }
            if (gp != null) {
                var mapa = mc.getSkinManager().getInsecureSkinInformation(gp);
                var tx = mapa.get(com.mojang.authlib.minecraft.MinecraftProfileTexture.Type.SKIN);
                if (tx != null) return new Skin(mc.getSkinManager().registerTexture(tx, com.mojang.authlib.minecraft.MinecraftProfileTexture.Type.SKIN),
                        "slim".equals(tx.getMetadata("model")));
                java.util.UUID id = net.minecraft.core.UUIDUtil.getOrCreatePlayerUUID(gp);
                return new Skin(net.minecraft.client.resources.DefaultPlayerSkin.getDefaultSkin(id), "slim".equals(net.minecraft.client.resources.DefaultPlayerSkin.getSkinModelName(id)));
            }
            return new Skin(net.minecraft.client.resources.DefaultPlayerSkin.getDefaultSkin(), false);
        }
        return null;
    }
    /** id -> {distancia acumulada, velocidad suave, último tick} para la animación de caminar */
    private static final Map<Integer, float[]> mov = new HashMap<>();

    static void cargar() {
        if (cuerpos != null) return;
        cuerpos = new HashMap<>();
        caras = new HashMap<>();
        try (InputStream in = PersonaRender.class.getResourceAsStream("/canon_personas.txt")) {
            if (in == null) return;
            BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8));
            String l;
            while ((l = r.readLine()) != null) {
                String[] p = l.split("\\|");
                if (p.length != 4) continue;
                (p[0].equals("B") ? cuerpos : caras).put(Integer.parseInt(p[1]), new Pieza(p[2], p[3]));
            }
        } catch (Exception ignored) {
        }
    }

    static int cmd(Display.ItemDisplay d) {
        Display.ItemDisplay.ItemRenderState st = d.itemRenderState();
        if (st == null) return -1;
        ItemStack s = st.itemStack();
        CompoundTag t = s.getTag();
        return t == null ? -1 : t.getInt("CustomModelData");
    }

    @SubscribeEvent
    public static void dibujar(RenderLivingEvent.Pre<?, ?> e) {
        LivingEntity ent = e.getEntity();
        if (!(ent instanceof Zombie) || !ent.isInvisible() || ent.getPassengers().isEmpty()) return;
        cargar();
        Pieza cuerpo = null, cara = null;
        float escala = 1f;
        for (Entity p : ent.getPassengers()) {
            if (!(p instanceof Display.ItemDisplay d)) continue;
            int c = cmd(d);
            Pieza b = cuerpos.get(c);
            if (b != null) {
                cuerpo = b;
                Display.RenderState rs = d.renderState();
                if (rs != null) {
                    Transformation tr = rs.transformation().get(e.getPartialTick());
                    escala = Math.max(0.2f, tr.getScale().y());
                }
            }
            Pieza h = caras.get(c);
            if (h != null) cara = h;
        }
        if (cuerpo == null) return;
        e.setCanceled(true);
        if (modelo == null) {
            modelo = new PlayerModel<>(Minecraft.getInstance().getEntityModels().bakeLayer(ModelLayers.PLAYER), false);
            modeloFino = new PlayerModel<>(Minecraft.getInstance().getEntityModels().bakeLayer(ModelLayers.PLAYER_SLIM), true);
        }
        ResourceLocation rl;
        PlayerModel<LivingEntity> md = modelo;
        if (cuerpo.quien().equals("@doble")) {
            // el doble: la skin de verdad de la víctima (sacada de la cabeza que lleva puesta), y la cabeza se esconde
            Skin sk = dobles.get(ent.getId());
            if (sk == null) {
                sk = skinDe(ent);
                if (sk == null) sk = new Skin(net.minecraft.client.resources.DefaultPlayerSkin.getDefaultSkin(), false);
                if (dobles.size() > 64) dobles.clear();
                dobles.put(ent.getId(), sk);
            }
            rl = sk.tex();
            if (sk.fino()) md = modeloFino;
            for (Entity p : ent.getPassengers())
                if (p instanceof Display.ItemDisplay d && d.itemRenderState() != null && d.itemRenderState().itemStack().is(Items.PLAYER_HEAD))
                    d.getSlot(0).set(ItemStack.EMPTY);
        } else {
            String tex = (cara != null && cara.quien().equals(cuerpo.quien())) ? cuerpo.quien() + "_skin_" + cara.que() : cuerpo.quien() + "_skin";
            rl = new ResourceLocation("canon", "textures/item/modelo/" + tex + ".png");
        }

        float pt = e.getPartialTick();
        float edad = ent.tickCount + pt;
        // caminar/correr: según lo que se movió de verdad en cada tick (no depende de los FPS)
        float[] m = mov.computeIfAbsent(ent.getId(), k -> new float[]{0f, 0f, -1f});
        float vx = (float) (ent.getX() - ent.xo), vz = (float) (ent.getZ() - ent.zo);
        float vel = Mth.sqrt(vx * vx + vz * vz);
        if (vel > 2f) vel = 0f; // teletransporte
        if (m[2] != ent.tickCount) {
            m[0] += vel;
            m[1] += (vel - m[1]) * 0.35f;
            m[2] = ent.tickCount;
        }
        if (mov.size() > 400) mov.clear();
        String pose = cuerpo.que();
        boolean corre = pose.startsWith("run") || m[1] > 0.24f;
        float amp = Math.max(Mth.clamp(m[1] * 6f, 0f, 1f), (pose.startsWith("walk") || pose.startsWith("run")) ? 0.6f : 0f);
        float fase = (m[0] + vel * pt) * (corre ? 3.2f : 4f) + (amp > 0.5f && m[1] < 0.02f ? edad * 0.35f : 0f);

        md.young = false;
        md.crouching = false;
        md.riding = false;
        md.attackTime = 0;
        md.setupAnim(ent, fase, amp * (corre ? 1.4f : 1f), edad, 0f, 0f);
        posar(md, pose, edad, cara == null ? "" : cara.que());
        md.hat.copyFrom(md.head);
        md.jacket.copyFrom(md.body);
        md.leftSleeve.copyFrom(md.leftArm);
        md.rightSleeve.copyFrom(md.rightArm);
        md.leftPants.copyFrom(md.leftLeg);
        md.rightPants.copyFrom(md.rightLeg);

        PoseStack ps = e.getPoseStack();
        ps.pushPose();
        float yaw = Mth.rotLerp(pt, ent.yRotO, ent.getYRot());
        float flota = pose.equals("float") ? Mth.sin(edad * 0.08f) * 0.12f + 0.25f : 0f;
        ps.translate(0, flota - (pose.equals("sit") ? 0.55f * escala : 0f), 0);
        ps.mulPose(Axis.YP.rotationDegrees(180f - yaw));
        if (corre) ps.mulPose(Axis.XP.rotationDegrees(-13f)); // corriendo: inclinado hacia adelante
        ps.scale(-1f, -1f, 1f);
        ps.scale(0.9375f * escala, 0.9375f * escala, 0.9375f * escala);
        ps.translate(0f, -1.501f, 0f);
        md.renderToBuffer(ps, e.getMultiBufferSource().getBuffer(RenderType.entityTranslucent(rl)), e.getPackedLight(),
                LivingEntityRenderer.getOverlayCoords(ent, 0f), 1f, 1f, 1f, 1f);
        ps.popPose();
    }

    /** Poses del datapack -> rotaciones del modelo de jugador, con un poco de vida. */
    static void posar(PlayerModel<LivingEntity> md, String pose, float edad, String cara) {
        float resp = Mth.sin(edad * 0.07f) * 0.04f;
        md.rightArm.zRot += resp;
        md.leftArm.zRot -= resp;
        md.head.xRot += Mth.sin(edad * 0.05f) * 0.03f;
        switch (pose) {
            case "reach", "brazos" -> {
                md.rightArm.xRot = -1.45f + Mth.sin(edad * 0.2f) * 0.05f;
                md.leftArm.xRot = -1.45f - Mth.sin(edad * 0.2f) * 0.05f;
            }
            case "arms_up" -> {
                md.rightArm.zRot = 2.6f;
                md.leftArm.zRot = -2.6f;
            }
            case "dance_a", "dance_b" -> {
                float t = edad * 0.25f;
                md.rightArm.zRot = 1.6f + Mth.sin(t) * 0.8f;
                md.leftArm.zRot = -1.6f + Mth.cos(t) * 0.8f;
                md.rightLeg.zRot = Math.max(0f, Mth.sin(t)) * 0.4f;
                md.leftLeg.zRot = -Math.max(0f, -Mth.sin(t)) * 0.4f;
                md.body.yRot = Mth.sin(t * 0.5f) * 0.3f;
                md.head.zRot = Mth.sin(t) * 0.2f;
            }
            case "laugh" -> {
                md.rightArm.xRot = -0.5f;
                md.leftArm.xRot = -0.5f;
                md.head.xRot = -0.3f + Mth.sin(edad * 0.9f) * 0.08f;
            }
            case "offer" -> md.rightArm.xRot = -1.2f;
            case "point" -> {
                md.rightArm.xRot = -1.55f;
                md.leftArm.xRot = 0.25f;
            }
            case "float" -> {
                md.rightArm.zRot = 0.6f + Mth.sin(edad * 0.05f) * 0.1f;
                md.leftArm.zRot = -0.6f - Mth.sin(edad * 0.05f) * 0.1f;
                md.rightLeg.xRot = 0.35f;
                md.leftLeg.xRot = 0.15f;
                md.head.xRot = 0.3f;
            }
            case "twist" -> {
                md.rightArm.zRot = 2.2f;
                md.leftArm.zRot = 0.9f;
                md.head.zRot = 0.9f;
                md.rightLeg.zRot = -0.4f;
            }
            case "cover" -> {
                md.rightArm.xRot = -2.3f;
                md.leftArm.xRot = -2.3f;
                md.rightArm.yRot = -0.5f;
                md.leftArm.yRot = 0.5f;
                md.head.xRot = 0.4f + Mth.sin(edad * 0.6f) * 0.04f;
            }
            case "sit" -> {
                md.rightLeg.xRot = -1.45f;
                md.leftLeg.xRot = -1.45f;
                md.rightLeg.yRot = 0.1f;
                md.leftLeg.yRot = -0.1f;
            }
            default -> {
            }
        }
        // caras de miedo: tirones de cabeza
        if (cara.contains("creepy") || cara.contains("void") || cara.contains("vacia") || cara.contains("glitch") || cara.contains("loco") || cara.contains("raro")) {
            if ((int) edad % 37 < 3) {
                md.head.zRot += Mth.sin(edad * 3.1f) * 0.6f;
                md.head.yRot += Mth.cos(edad * 2.3f) * 0.3f;
            }
            md.head.zRot += 0.25f;
        }
    }
}
