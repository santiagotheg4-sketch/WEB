package com.canonevent;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Nicolás en 3D con su skin (cara de burla, de odio o gritando), boca abajo en el techo y con los brazos estirados cuando corre. */
public class NicolasRender extends MobRenderer<Nicolas, PlayerModel<Nicolas>> {
    static final String[] CARAS = {"burla", "odio", "grito"};

    public NicolasRender(EntityRendererProvider.Context c) {
        super(c, new Modelo(c.bakeLayer(ModelLayers.PLAYER)), 0.5f);
        // ojos blancos que brillan en la oscuridad
        this.addLayer(new net.minecraft.client.renderer.entity.layers.EyesLayer<>(this) {
            final net.minecraft.client.renderer.RenderType t = net.minecraft.client.renderer.RenderType.eyes(new ResourceLocation(CanonEvent.MODID, "textures/entity/nicolas_ojos.png"));
            @Override public net.minecraft.client.renderer.RenderType renderType() { return t; }
        });
    }

    static class Modelo extends PlayerModel<Nicolas> {
        Modelo(net.minecraft.client.model.geom.ModelPart p) { super(p, false); }

        @Override
        public void setupAnim(Nicolas e, float paso, float cant, float edad, float yaw, float pitch) {
            super.setupAnim(e, paso, cant, edad, yaw, pitch);
            int est = e.estado();
            if (est == Nicolas.CORRE) { // brazos estirados hacia ti, cabeza ladeada
                rightArm.xRot = -1.5f + Mth.cos(paso * 0.9f) * 0.25f * cant;
                leftArm.xRot = -1.5f - Mth.cos(paso * 0.9f) * 0.25f * cant;
                head.zRot = 0.35f;
            } else if (est == Nicolas.TECHO) { // colgado: brazos hacia abajo (hacia ti), meciéndose
                rightArm.xRot = Mth.PI + Mth.sin(edad * 0.1f) * 0.15f;
                leftArm.xRot = Mth.PI - Mth.sin(edad * 0.1f) * 0.15f;
                rightLeg.xRot = leftLeg.xRot = 0;
            } else if (est == Nicolas.AGARRA) { // agarrado de los bordes del hueco, con las dos manos
                rightArm.xRot = -2.05f + Mth.sin(edad * 0.9f) * 0.03f;
                leftArm.xRot = -2.05f - Mth.sin(edad * 0.9f) * 0.03f;
                rightArm.zRot = 0.42f;
                leftArm.zRot = -0.42f;
                head.xRot = 0.05f;
                head.zRot = 0.18f + Mth.sin(edad * 0.15f) * 0.08f;
            } else if (est == Nicolas.LEJOS) { // quieto, la cabeza ladeándose despacio
                rightArm.xRot = leftArm.xRot = 0;
                rightArm.zRot = 0.05f;
                leftArm.zRot = -0.05f;
                head.zRot = Mth.sin(edad * 0.04f) * 0.45f;
            } else if (est == Nicolas.APAGA) {
                rightArm.xRot = -0.9f;
            }
            if ((int) edad % 31 < 2) { // tirones de cabeza
                head.zRot += Mth.sin(edad * 3f) * 0.6f;
                head.yRot += 0.4f;
            }
            hat.copyFrom(head);
            jacket.copyFrom(body);
            leftSleeve.copyFrom(leftArm);
            rightSleeve.copyFrom(rightArm);
            leftPants.copyFrom(leftLeg);
            rightPants.copyFrom(rightLeg);
        }
    }

    @Override
    protected void setupRotations(Nicolas e, PoseStack ps, float edad, float yaw, float pt) {
        super.setupRotations(e, ps, edad, yaw, pt);
        if (e.estado() == Nicolas.TECHO) { // boca abajo, con los pies en el techo
            ps.translate(0, e.getBbHeight() + 0.1f, 0);
            ps.mulPose(Axis.ZP.rotationDegrees(180f));
        }
        if (e.estado() == Nicolas.CORRE) ps.mulPose(Axis.XP.rotationDegrees(-14f)); // corre inclinado hacia adelante
    }

    static final ResourceLocation OJOS = new ResourceLocation(CanonEvent.MODID, "textures/entity/nicolas_ojos.png");

    /** Dos puntitos blancos que brillan: se le ven los ojos desde lejos en la oscuridad. */
    @Override
    public void render(Nicolas e, float yaw, float pt, PoseStack ps, net.minecraft.client.renderer.MultiBufferSource b, int luz) {
        super.render(e, yaw, pt, ps, b, luz);
        int est = e.estado();
        if (e.isInvisible() || est == Nicolas.TECHO || est == Nicolas.CORRE) return;
        float hy = Mth.rotLerp(pt, e.yHeadRotO, e.yHeadRot) * Mth.DEG_TO_RAD;
        float fx = -Mth.sin(hy), fz = Mth.cos(hy);   // hacia donde mira
        float rx = fz, rz = -fx;                      // a su lado
        com.mojang.blaze3d.vertex.VertexConsumer vc = b.getBuffer(net.minecraft.client.renderer.RenderType.eyes(OJOS));
        float lado = 0.05f, u = 9.5f / 64f, v = 12.5f / 64f;
        for (float sgn : new float[]{-1f, 1f}) {
            ps.pushPose();
            ps.translate(fx * 0.27f + rx * 0.117f * sgn, 1.6f, fz * 0.27f + rz * 0.117f * sgn);
            ps.mulPose(this.entityRenderDispatcher.cameraOrientation());
            org.joml.Matrix4f m = ps.last().pose();
            float[][] q = {{-lado, -lado}, {lado, -lado}, {lado, lado}, {-lado, lado}};
            for (int cara = 0; cara < 2; cara++)
                for (int i = 0; i < 4; i++) {
                    float[] c = q[cara == 0 ? i : 3 - i];
                    vc.vertex(m, c[0], c[1], 0).color(255, 255, 255, 255).uv(u, v)
                            .overlayCoords(net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(0, 0, 1).endVertex();
                }
            ps.popPose();
        }
    }

    @Override
    protected void scale(Nicolas e, PoseStack ps, float pt) {
        ps.scale(0.9375f, 0.9375f, 0.9375f);
    }

    /** Sin letrero con el nombre encima: da más miedo sin saber qué es. */
    @Override
    protected boolean shouldShowName(Nicolas e) {
        return false;
    }

    @Override
    public ResourceLocation getTextureLocation(Nicolas e) {
        return new ResourceLocation("canon", "textures/item/modelo/nicolas_skin_" + CARAS[Mth.clamp(e.cara(), 0, 2)] + ".png");
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistroNicolas {
        @SubscribeEvent
        public static void renderNicolas(EntityRenderersEvent.RegisterRenderers e) {
            e.registerEntityRenderer(CanonEntidades.NICOLAS.get(), NicolasRender::new);
        }
    }
}
