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

    @Override
    protected void scale(Nicolas e, PoseStack ps, float pt) {
        ps.scale(0.9375f, 0.9375f, 0.9375f);
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
