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
 * La Masa en 3D: un torso enorme inclinado con joroba y espinas, cabeza colgando hacia adelante con la mandíbula
 * abierta, dos brazos larguísimos con garras con los que se arrastra, patas de atrás dobladas y dos bracitos
 * que le salen de la espalda y se retuercen. Textura 128x128 (la genera tools/features/masa.py).
 */
public class MasaModelo extends EntityModel<Masa> {
    public static final ModelLayerLocation CAPA = new ModelLayerLocation(new ResourceLocation(CanonEvent.MODID, "masa"), "main");
    private final ModelPart raiz, torso, cabeza, mandibula, brazoD, brazoI, anteD, anteI, piernaD, piernaI, canillaD, canillaI, espaldaD, espaldaI;

    public MasaModelo(ModelPart r) {
        this.raiz = r;
        this.torso = r.getChild("torso");
        this.cabeza = torso.getChild("cabeza");
        this.mandibula = cabeza.getChild("mandibula");
        this.espaldaD = torso.getChild("espalda_d");
        this.espaldaI = torso.getChild("espalda_i");
        this.brazoD = r.getChild("brazo_d");
        this.brazoI = r.getChild("brazo_i");
        this.anteD = brazoD.getChild("ante");
        this.anteI = brazoI.getChild("ante");
        this.piernaD = r.getChild("pierna_d");
        this.piernaI = r.getChild("pierna_i");
        this.canillaD = piernaD.getChild("canilla");
        this.canillaI = piernaI.getChild("canilla");
    }

    static CubeListBuilder garra() {
        return CubeListBuilder.create().texOffs(72, 66).addBox(-1.5f, 0, -1.5f, 3, 22, 3)
                .texOffs(96, 66).addBox(-2.5f, 21, -1.5f, 1, 6, 1)
                .texOffs(96, 66).addBox(-0.5f, 21, -2.5f, 1, 7, 1)
                .texOffs(96, 66).addBox(1.5f, 21, -1.5f, 1, 6, 1);
    }

    public static LayerDefinition crear() {
        MeshDefinition m = new MeshDefinition();
        PartDefinition p = m.getRoot();
        PartDefinition torso = p.addOrReplaceChild("torso", CubeListBuilder.create()
                .texOffs(0, 0).addBox(-11, -22, -11, 22, 22, 22)
                .texOffs(0, 44).addBox(-8, -28, -2, 16, 8, 14)
                .texOffs(96, 92).addBox(-1, -33, 0, 2, 5, 2)
                .texOffs(96, 92).addBox(-1, -34, 5, 2, 6, 2)
                .texOffs(96, 92).addBox(-1, -32, 10, 2, 5, 2)
                .texOffs(96, 92).addBox(4, -31, 3, 2, 4, 2)
                .texOffs(96, 92).addBox(-6, -31, 7, 2, 4, 2),
                PartPose.offsetAndRotation(0, 2, 4, 0.35f, 0, 0));
        PartDefinition cabeza = torso.addOrReplaceChild("cabeza", CubeListBuilder.create()
                .texOffs(60, 44).addBox(-6, -5, -12, 12, 10, 12)
                .texOffs(108, 66).addBox(-5, 5, -11.5f, 1, 2, 1)
                .texOffs(108, 66).addBox(-2.5f, 5, -11.8f, 1, 3, 1)
                .texOffs(108, 66).addBox(1.5f, 5, -11.8f, 1, 3, 1)
                .texOffs(108, 66).addBox(4, 5, -11.5f, 1, 2, 1),
                PartPose.offset(0, -12, -10));
        cabeza.addOrReplaceChild("mandibula", CubeListBuilder.create()
                .texOffs(0, 66).addBox(-5, 0, -10, 10, 4, 10)
                .texOffs(108, 66).addBox(-4, -2, -9.5f, 1, 2, 1)
                .texOffs(108, 66).addBox(-1.5f, -3, -9.8f, 1, 3, 1)
                .texOffs(108, 66).addBox(0.5f, -2, -9.8f, 1, 2, 1)
                .texOffs(108, 66).addBox(3, -3, -9.5f, 1, 3, 1),
                PartPose.offset(0, 5, -1));
        torso.addOrReplaceChild("espalda_d", CubeListBuilder.create().texOffs(80, 92).addBox(-1, -16, -1, 2, 16, 2), PartPose.offset(-6, -24, 4));
        torso.addOrReplaceChild("espalda_i", CubeListBuilder.create().texOffs(88, 92).addBox(-1, -16, -1, 2, 16, 2), PartPose.offset(6, -24, 6));
        PartDefinition bd = p.addOrReplaceChild("brazo_d", CubeListBuilder.create().texOffs(40, 66).addBox(-2, -2, -2, 4, 18, 4), PartPose.offset(-13, -12, -9));
        bd.addOrReplaceChild("ante", garra(), PartPose.offset(0, 15, 0));
        PartDefinition bi = p.addOrReplaceChild("brazo_i", CubeListBuilder.create().texOffs(56, 66).addBox(-2, -2, -2, 4, 18, 4), PartPose.offset(13, -12, -9));
        bi.addOrReplaceChild("ante", garra(), PartPose.offset(0, 15, 0));
        PartDefinition pd = p.addOrReplaceChild("pierna_d", CubeListBuilder.create().texOffs(0, 88).addBox(-3, 0, -3, 6, 14, 6), PartPose.offset(-8, 0, 12));
        pd.addOrReplaceChild("canilla", CubeListBuilder.create().texOffs(48, 88).addBox(-2, 0, -2, 4, 14, 4), PartPose.offset(0, 13, 0));
        PartDefinition pi = p.addOrReplaceChild("pierna_i", CubeListBuilder.create().texOffs(24, 88).addBox(-3, 0, -3, 6, 14, 6), PartPose.offset(8, 0, 12));
        pi.addOrReplaceChild("canilla", CubeListBuilder.create().texOffs(64, 88).addBox(-2, 0, -2, 4, 14, 4), PartPose.offset(0, 13, 0));
        return LayerDefinition.create(m, 128, 128);
    }

    @Override
    public void setupAnim(Masa e, float paso, float cantidad, float edad, float yaw, float pitch) {
        boolean corre = e.corre();
        float amt = Math.min(1f, cantidad * (corre ? 1.3f : 1f));
        float f = paso * (corre ? 0.55f : 0.4f);
        float golpe = Mth.sin(this.attackTime * Mth.PI);

        // torso: respira, se balancea al galopar
        torso.y = 2 + Mth.sin(f * 2f) * 1.6f * amt + Mth.sin(edad * 0.09f) * 0.4f;
        torso.xRot = 0.35f + (corre ? 0.12f : 0f) + Mth.sin(edad * 0.08f) * 0.03f + golpe * 0.25f;
        torso.zRot = Mth.sin(f) * 0.09f * amt;

        // brazos de adelante: se arrastra con ellos, uno y otro; al golpear los levanta y los azota
        float bD = Mth.cos(f), bI = Mth.cos(f + Mth.PI);
        brazoD.xRot = -0.35f + bD * 0.85f * amt - golpe * 1.9f;
        brazoI.xRot = -0.35f + bI * 0.85f * amt - golpe * 1.9f;
        anteD.xRot = -0.35f - Math.max(0f, Mth.sin(f)) * 0.7f * amt + golpe * 0.6f;
        anteI.xRot = -0.35f - Math.max(0f, Mth.sin(f + Mth.PI)) * 0.7f * amt + golpe * 0.6f;
        brazoD.zRot = 0.18f + Mth.sin(edad * 0.05f) * 0.05f;
        brazoI.zRot = -0.18f - Mth.sin(edad * 0.05f) * 0.05f;
        brazoD.y = -12 + torso.y - 2;
        brazoI.y = -12 + torso.y - 2;

        // patas de atrás (dobladas como de perro), a contratiempo
        piernaD.xRot = -0.6f + bI * 0.6f * amt;
        piernaI.xRot = -0.6f + bD * 0.6f * amt;
        canillaD.xRot = 1.0f + Math.max(0f, Mth.sin(f + Mth.PI)) * 0.5f * amt;
        canillaI.xRot = 1.0f + Math.max(0f, Mth.sin(f)) * 0.5f * amt;

        // cabeza: te mira, tirones raros; mandíbula que se abre y cierra
        cabeza.yRot = Mth.clamp(yaw, -60f, 60f) * Mth.DEG_TO_RAD;
        cabeza.xRot = -0.3f + pitch * Mth.DEG_TO_RAD * 0.5f;
        float tiron = ((int) edad % 37 < 3) ? Mth.sin(edad * 2.9f) * 0.6f : 0f;
        cabeza.zRot = Mth.sin(edad * 0.04f) * 0.15f + tiron;
        mandibula.xRot = 0.35f + Mth.sin(edad * 0.13f) * 0.18f + (corre ? 0.3f : 0f) + golpe * 0.6f;

        // los bracitos de la espalda: se retuercen sin parar
        espaldaD.xRot = Mth.sin(edad * 0.31f) * 0.5f - 0.3f;
        espaldaD.zRot = -0.5f + Mth.sin(edad * 0.23f + 1f) * 0.35f;
        espaldaI.xRot = Mth.sin(edad * 0.27f + 2f) * 0.5f - 0.2f;
        espaldaI.zRot = 0.5f + Mth.sin(edad * 0.19f) * 0.35f;
        if ((int) edad % 23 < 2) {
            espaldaD.zRot += 0.6f;
            espaldaI.xRot -= 0.5f;
        }
    }

    @Override
    public void renderToBuffer(PoseStack ps, VertexConsumer vc, int luz, int overlay, float r, float g, float b, float a) {
        raiz.render(ps, vc, luz, overlay, r, g, b, a);
    }
}
