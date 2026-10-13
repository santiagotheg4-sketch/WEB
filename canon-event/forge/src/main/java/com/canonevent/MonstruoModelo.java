package com.canonevent;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

/**
 * Cuerpo 3D de Diana (y del gigante): 3 bloques de alto, piernas largas, brazos que llegan a las rodillas,
 * cuello largo torcido hacia adelante, pelo que le tapa la cara, falda rota. Textura 128x128 (la genera tools/build.py).
 */
public class MonstruoModelo extends EntityModel<Monstruo> {
    public static final ModelLayerLocation CAPA = new ModelLayerLocation(new ResourceLocation(CanonEvent.MODID, "monstruo"), "main");
    private final ModelPart raiz, cuerpo, cuello, cabeza, brazoD, brazoI, piernaD, piernaI;

    public MonstruoModelo(ModelPart r) {
        this.raiz = r;
        this.cuerpo = r.getChild("cuerpo");
        this.cuello = cuerpo.getChild("cuello");
        this.cabeza = cuello.getChild("cabeza");
        this.brazoD = cuerpo.getChild("brazo_d");
        this.brazoI = cuerpo.getChild("brazo_i");
        this.piernaD = r.getChild("pierna_d");
        this.piernaI = r.getChild("pierna_i");
    }

    public static LayerDefinition crear() {
        MeshDefinition m = new MeshDefinition();
        PartDefinition p = m.getRoot();
        p.addOrReplaceChild("pierna_d", CubeListBuilder.create().texOffs(0, 0).addBox(-1.5f, 0, -1.5f, 3, 20, 3), PartPose.offset(-2.5f, 4, 0));
        p.addOrReplaceChild("pierna_i", CubeListBuilder.create().texOffs(12, 0).addBox(-1.5f, 0, -1.5f, 3, 20, 3), PartPose.offset(2.5f, 4, 0));
        PartDefinition cuerpo = p.addOrReplaceChild("cuerpo", CubeListBuilder.create().texOffs(24, 0).addBox(-4, 0, -2, 8, 14, 4)
                .texOffs(0, 40).addBox(-5, 10, -3, 10, 9, 6), PartPose.offset(0, -10, 0));
        cuerpo.addOrReplaceChild("brazo_d", CubeListBuilder.create().texOffs(48, 0).addBox(-1, -1, -1, 2, 28, 2), PartPose.offset(-5, 1, 0));
        cuerpo.addOrReplaceChild("brazo_i", CubeListBuilder.create().texOffs(56, 0).addBox(-1, -1, -1, 2, 28, 2), PartPose.offset(5, 1, 0));
        PartDefinition cuello = cuerpo.addOrReplaceChild("cuello", CubeListBuilder.create().texOffs(64, 0).addBox(-1, -7, -1, 2, 7, 2), PartPose.offset(0, 0, 0));
        cuello.addOrReplaceChild("cabeza", CubeListBuilder.create().texOffs(72, 0).addBox(-4, -8, -4, 8, 8, 8)
                .texOffs(0, 60).addBox(-4.5f, -8.5f, -4.6f, 9, 14, 1)
                .texOffs(24, 60).addBox(-4.5f, -8.5f, 3.6f, 9, 16, 1), PartPose.offset(0, -7, 0));
        return LayerDefinition.create(m, 128, 128);
    }

    @Override
    public void setupAnim(Monstruo e, float paso, float cantidad, float edad, float yaw, float pitch) {
        boolean corre = e.persigue();
        float camina = Mth.cos(paso * 0.45f) * 1.1f * cantidad;
        piernaD.xRot = camina;
        piernaI.xRot = -camina;
        cuerpo.xRot = corre ? 0.45f : 0.18f;
        cuello.xRot = corre ? 0.2f : 0.55f;
        // la cabeza: mira al jugador, ladeada, y cada tanto da un tirón
        cabeza.yRot = yaw * Mth.DEG_TO_RAD;
        cabeza.xRot = pitch * Mth.DEG_TO_RAD * 0.5f - 0.3f;
        float tiron = ((int) edad % 41 < 3) ? Mth.sin(edad * 2.7f) * 0.7f : 0f;
        cabeza.zRot = 0.38f + tiron;
        // los brazos cuelgan y se mecen; cuando corre, se estiran hacia ti
        float meneo = Mth.sin(edad * 0.06f) * 0.06f;
        if (corre) {
            brazoD.xRot = -1.35f + Mth.cos(paso * 0.45f) * 0.25f * cantidad;
            brazoI.xRot = -1.35f - Mth.cos(paso * 0.45f) * 0.25f * cantidad;
        } else {
            brazoD.xRot = -camina * 0.3f + meneo;
            brazoI.xRot = camina * 0.3f - meneo;
        }
        brazoD.zRot = 0.08f + meneo;
        brazoI.zRot = -0.08f - meneo;
    }

    @Override
    public void renderToBuffer(PoseStack ps, VertexConsumer vc, int luz, int overlay, float r, float g, float b, float a) {
        raiz.render(ps, vc, luz, overlay, r, g, b, a);
    }
}
