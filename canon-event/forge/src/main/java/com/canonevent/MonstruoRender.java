package com.canonevent;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Dibuja a Diana y al gigante (el gigante es el mismo cuerpo, 4 veces más grande y con otra piel). */
public class MonstruoRender extends MobRenderer<Monstruo, MonstruoModelo> {
    private static final ResourceLocation DIANA = new ResourceLocation(CanonEvent.MODID, "textures/entity/diana.png");
    private static final ResourceLocation GIGANTE = new ResourceLocation(CanonEvent.MODID, "textures/entity/gigante.png");
    private final float escala;

    public MonstruoRender(EntityRendererProvider.Context c, float escala) {
        super(c, new MonstruoModelo(c.bakeLayer(MonstruoModelo.CAPA)), 0.5f * escala);
        this.escala = escala;
        this.addLayer(new Ojos(this));
    }

    /** Ojos y sonrisa de Diana que brillan en la oscuridad. */
    static class Ojos extends net.minecraft.client.renderer.entity.layers.EyesLayer<Monstruo, MonstruoModelo> {
        static final net.minecraft.client.renderer.RenderType TIPO = net.minecraft.client.renderer.RenderType.eyes(new ResourceLocation(CanonEvent.MODID, "textures/entity/diana_ojos.png"));
        Ojos(MonstruoRender r) { super(r); }
        @Override public net.minecraft.client.renderer.RenderType renderType() { return TIPO; }
        @Override public void render(PoseStack ps, net.minecraft.client.renderer.MultiBufferSource b, int luz, Monstruo e, float a, float c, float d, float f, float g, float h) {
            if (e.tipo == Monstruo.Tipo.DIANA) super.render(ps, b, luz, e, a, c, d, f, g, h);
        }
    }

    @Override
    protected void scale(Monstruo e, PoseStack ps, float pt) {
        ps.scale(escala, escala, escala);
    }

    @Override
    public ResourceLocation getTextureLocation(Monstruo e) {
        return e.tipo == Monstruo.Tipo.GIGANTE ? GIGANTE : DIANA;
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistroMonstruos {
        @SubscribeEvent
        public static void capasMonstruos(EntityRenderersEvent.RegisterLayerDefinitions e) {
            e.registerLayerDefinition(MonstruoModelo.CAPA, MonstruoModelo::crear);
        }

        @SubscribeEvent
        public static void renderMonstruos(EntityRenderersEvent.RegisterRenderers e) {
            e.registerEntityRenderer(CanonEntidades.DIANA.get(), c -> new MonstruoRender(c, 1.0f));
            e.registerEntityRenderer(CanonEntidades.GIGANTE.get(), c -> new MonstruoRender(c, 4.0f));
        }
    }
}
