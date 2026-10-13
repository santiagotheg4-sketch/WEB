package com.canonevent;

import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Dibuja a La Masa, con los ojos (y la boca por dentro) brillando en la oscuridad de las catacumbas. */
public class MasaRender extends MobRenderer<Masa, MasaModelo> {
    private static final ResourceLocation PIEL = new ResourceLocation(CanonEvent.MODID, "textures/entity/masa.png");

    public MasaRender(EntityRendererProvider.Context c) {
        super(c, new MasaModelo(c.bakeLayer(MasaModelo.CAPA)), 1.3f);
        this.addLayer(new EyesLayer<>(this) {
            final RenderType tipo = RenderType.eyes(new ResourceLocation(CanonEvent.MODID, "textures/entity/masa_ojos.png"));

            @Override
            public RenderType renderType() {
                return tipo;
            }
        });
    }

    @Override
    protected void scale(Masa e, PoseStack ps, float pt) {
        ps.scale(1.1f, 1.1f, 1.1f);
    }

    @Override
    public ResourceLocation getTextureLocation(Masa e) {
        return PIEL;
    }

    @Mod.EventBusSubscriber(modid = CanonEvent.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
    public static class RegistroMasa {
        @SubscribeEvent
        public static void capasMasa(EntityRenderersEvent.RegisterLayerDefinitions e) {
            e.registerLayerDefinition(MasaModelo.CAPA, MasaModelo::crear);
        }

        @SubscribeEvent
        public static void renderMasa(EntityRenderersEvent.RegisterRenderers e) {
            e.registerEntityRenderer(CanonEntidades.MASA.get(), MasaRender::new);
        }
    }
}
