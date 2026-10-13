package com.canonevent;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.culling.Frustum;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Cómo se ven las criaturas del agua (con ojos que brillan en la oscuridad). */
public class MarRender {
    static ResourceLocation tex(String n) {
        return new ResourceLocation(CanonEvent.MODID, "textures/entity/" + n + ".png");
    }

    public static class Ahogada extends MobRenderer<Marina, MarModelos.Ahogada> {
        public Ahogada(EntityRendererProvider.Context c) {
            super(c, new MarModelos.Ahogada(c.bakeLayer(MarModelos.Ahogada.CAPA)), 0.4f);
            this.addLayer(new EyesLayer<>(this) {
                final RenderType t = RenderType.eyes(tex("ahogada_ojos"));
                @Override public RenderType renderType() { return t; }
            });
        }

        @Override public ResourceLocation getTextureLocation(Marina e) { return tex("ahogada"); }
        @Override protected boolean shouldShowName(Marina e) { return false; }
    }

    public static class Leviatan extends MobRenderer<Marina, MarModelos.Leviatan> {
        public Leviatan(EntityRendererProvider.Context c) {
            super(c, new MarModelos.Leviatan(c.bakeLayer(MarModelos.Leviatan.CAPA)), 0f);
            this.addLayer(new EyesLayer<>(this) {
                final RenderType t = RenderType.eyes(tex("leviatan_ojos"));
                @Override public RenderType renderType() { return t; }
            });
        }

        @Override protected void scale(Marina e, PoseStack ps, float pt) { ps.scale(2.2f, 2.2f, 2.2f); }

        /** Es enorme: que no desaparezca cuando la cabeza (la caja de choque) queda fuera de la pantalla. */
        @Override public boolean shouldRender(Marina e, Frustum f, double x, double y, double z) {
            return f.isVisible(e.getBoundingBox().inflate(20));
        }

        @Override public ResourceLocation getTextureLocation(Marina e) { return tex("leviatan"); }
        @Override protected boolean shouldShowName(Marina e) { return false; }
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistroMar {
        @SubscribeEvent
        public static void capasMar(EntityRenderersEvent.RegisterLayerDefinitions e) {
            e.registerLayerDefinition(MarModelos.Ahogada.CAPA, MarModelos.Ahogada::crear);
            e.registerLayerDefinition(MarModelos.Leviatan.CAPA, MarModelos.Leviatan::crear);
        }

        @SubscribeEvent
        public static void renderMar(EntityRenderersEvent.RegisterRenderers e) {
            e.registerEntityRenderer(CanonEntidades.AHOGADA.get(), Ahogada::new);
            e.registerEntityRenderer(CanonEntidades.LEVIATAN.get(), Leviatan::new);
        }
    }
}
