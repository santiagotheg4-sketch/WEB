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

/** Los cuerpos 3D de las criaturas del agua. Texturas 128x128 (las genera tools/features/mar.py). */
public class MarModelos {

    /** La Ahogada: flaca, pálida, vestido roto, brazos largos con dedos largos y el pelo mojado tapándole la cara. */
    public static class Ahogada extends EntityModel<Marina> {
        public static final ModelLayerLocation CAPA = new ModelLayerLocation(new ResourceLocation(CanonEvent.MODID, "ahogada"), "main");
        private final ModelPart todo, cabeza, brazoD, brazoI, dedosD, dedosI, piernaD, piernaI, torso;

        public Ahogada(ModelPart r) {
            this.todo = r.getChild("todo");
            this.torso = todo.getChild("torso");
            this.cabeza = torso.getChild("cabeza");
            this.brazoD = torso.getChild("brazo_d");
            this.brazoI = torso.getChild("brazo_i");
            this.dedosD = brazoD.getChild("dedos");
            this.dedosI = brazoI.getChild("dedos");
            this.piernaD = todo.getChild("pierna_d");
            this.piernaI = todo.getChild("pierna_i");
        }

        static CubeListBuilder dedos() {
            return CubeListBuilder.create().texOffs(16, 44).addBox(-1.2f, 0, -0.5f, 1, 6, 1).texOffs(16, 44).addBox(0, 0, -1, 1, 7, 1)
                    .texOffs(16, 44).addBox(0.4f, 0, 0.3f, 1, 5, 1);
        }

        public static LayerDefinition crear() {
            MeshDefinition m = new MeshDefinition();
            PartDefinition todo = m.getRoot().addOrReplaceChild("todo", CubeListBuilder.create(), PartPose.offset(0, 6, 0));
            PartDefinition torso = todo.addOrReplaceChild("torso", CubeListBuilder.create().texOffs(0, 24).addBox(-4, 0, -2, 8, 12, 4)
                    .texOffs(24, 24).addBox(-5, 8, -3, 10, 14, 6), PartPose.offset(0, -12, 0));
            torso.addOrReplaceChild("cabeza", CubeListBuilder.create().texOffs(0, 0).addBox(-4, -9, -4, 8, 9, 8)
                    .texOffs(32, 0).addBox(-4.5f, -9.5f, -4.6f, 9, 18, 1)
                    .texOffs(56, 0).addBox(-4.5f, -9.5f, 3.6f, 9, 22, 1)
                    .texOffs(80, 0).addBox(-4.6f, -9.5f, -4, 1, 16, 8)
                    .texOffs(80, 0).mirror().addBox(3.6f, -9.5f, -4, 1, 16, 8), PartPose.offset(0, 0, 0));
            PartDefinition bd = torso.addOrReplaceChild("brazo_d", CubeListBuilder.create().texOffs(0, 44).addBox(-1, -1, -1, 2, 24, 2), PartPose.offset(-5, 1, 0));
            bd.addOrReplaceChild("dedos", dedos(), PartPose.offset(0, 22, 0));
            PartDefinition bi = torso.addOrReplaceChild("brazo_i", CubeListBuilder.create().texOffs(8, 44).addBox(-1, -1, -1, 2, 24, 2), PartPose.offset(5, 1, 0));
            bi.addOrReplaceChild("dedos", dedos(), PartPose.offset(0, 22, 0));
            todo.addOrReplaceChild("pierna_d", CubeListBuilder.create().texOffs(24, 48).addBox(-1.5f, 0, -1.5f, 3, 18, 3), PartPose.offset(-2, 0, 0));
            todo.addOrReplaceChild("pierna_i", CubeListBuilder.create().texOffs(36, 48).addBox(-1.5f, 0, -1.5f, 3, 18, 3), PartPose.offset(2, 0, 0));
            return LayerDefinition.create(m, 128, 128);
        }

        @Override
        public void setupAnim(Marina e, float paso, float cantidad, float edad, float yaw, float pitch) {
            int est = e.estado();
            boolean llama = e.llama() > 0;
            todo.xRot = 0;
            todo.y = 6;
            cabeza.yRot = Mth.clamp(yaw, -70, 70) * Mth.DEG_TO_RAD;
            cabeza.xRot = pitch * Mth.DEG_TO_RAD * 0.5f + 0.15f;
            float tiron = ((int) edad % 43 < 3) ? Mth.sin(edad * 3.1f) * 0.7f : 0f;
            cabeza.zRot = 0.32f + tiron;
            // brazos flotando en el agua, abiertos y meciéndose
            float flota = Mth.sin(edad * 0.06f);
            brazoD.xRot = -0.2f + flota * 0.15f;
            brazoI.xRot = -0.2f - flota * 0.15f;
            brazoD.zRot = 0.45f + flota * 0.12f;
            brazoI.zRot = -0.45f - flota * 0.12f;
            brazoD.yRot = brazoI.yRot = 0;
            dedosD.xRot = dedosI.xRot = 0.2f + Mth.sin(edad * 0.2f) * 0.15f;
            piernaD.xRot = Mth.sin(edad * 0.07f) * 0.25f;
            piernaI.xRot = -Mth.sin(edad * 0.07f) * 0.25f;
            if (est == 4) { // en la orilla: de pie, brazos colgando, ladeada
                brazoD.zRot = 0.06f;
                brazoI.zRot = -0.06f;
                brazoD.xRot = brazoI.xRot = Mth.sin(edad * 0.05f) * 0.04f;
                piernaD.xRot = piernaI.xRot = 0;
            }
            if (llama && (est == 0 || est == 4)) { // te llama con la mano: ven... ven...
                brazoD.xRot = -1.55f + Mth.sin(edad * 0.22f) * 0.35f;
                brazoD.zRot = 0.05f;
                dedosD.xRot = 0.5f + Mth.sin(edad * 0.44f) * 0.7f;
                cabeza.zRot = 0.5f;
            }
            if (est == 1) { // nada hacia ti, horizontal, brazadas largas
                todo.xRot = 1.45f;
                float b = edad * 0.3f;
                brazoD.xRot = -2.6f + Mth.sin(b) * 0.9f;
                brazoI.xRot = -2.6f + Mth.sin(b + Mth.PI) * 0.9f;
                brazoD.zRot = 0.2f;
                brazoI.zRot = -0.2f;
                piernaD.xRot = Mth.sin(edad * 0.6f) * 0.5f;
                piernaI.xRot = -Mth.sin(edad * 0.6f) * 0.5f;
                cabeza.xRot = -1.0f;
            }
            if (est == 2) { // te agarra: te abraza para hundirte
                brazoD.xRot = brazoI.xRot = -1.9f + Mth.sin(edad * 1.3f) * 0.08f;
                brazoD.yRot = 0.5f;
                brazoI.yRot = -0.5f;
                brazoD.zRot = brazoI.zRot = 0;
                dedosD.xRot = dedosI.xRot = 1.2f;
                cabeza.xRot = -0.5f + Mth.sin(edad * 1.7f) * 0.1f;
                cabeza.zRot = Mth.sin(edad * 2.3f) * 0.3f;
            }
            if (est == 3) { // se hunde con los brazos para arriba
                brazoD.zRot = 2.7f + Mth.sin(edad * 0.2f) * 0.1f;
                brazoI.zRot = -2.7f - Mth.sin(edad * 0.2f) * 0.1f;
                cabeza.xRot = 0.6f;
            }
        }

        @Override
        public void renderToBuffer(PoseStack ps, VertexConsumer vc, int luz, int overlay, float r, float g, float b, float a) {
            todo.render(ps, vc, luz, overlay, r, g, b, a);
        }
    }

    /** El Leviatán: una serpiente de 15 bloques con cabeza enorme, mandíbula con dientes y espinas en el lomo. */
    public static class Leviatan extends EntityModel<Marina> {
        public static final ModelLayerLocation CAPA = new ModelLayerLocation(new ResourceLocation(CanonEvent.MODID, "leviatan"), "main");
        static final int N = 5;
        private final ModelPart cabeza, mandibula;
        private final ModelPart[] seg = new ModelPart[N + 1];

        public Leviatan(ModelPart r) {
            this.cabeza = r.getChild("cabeza");
            this.mandibula = cabeza.getChild("mandibula");
            ModelPart p = cabeza;
            for (int i = 0; i < N; i++) {
                p = p.getChild("seg" + i);
                seg[i] = p;
            }
            seg[N] = p.getChild("cola");
        }

        public static LayerDefinition crear() {
            MeshDefinition m = new MeshDefinition();
            PartDefinition cab = m.getRoot().addOrReplaceChild("cabeza", CubeListBuilder.create().texOffs(0, 0).addBox(-6, -5, -18, 12, 10, 18)
                    .texOffs(112, 0).addBox(-5, 5, -17, 1, 3, 1).texOffs(112, 0).addBox(-2, 5, -17.5f, 1, 4, 1)
                    .texOffs(112, 0).addBox(1, 5, -17.5f, 1, 4, 1).texOffs(112, 0).addBox(4, 5, -17, 1, 3, 1)
                    .texOffs(104, 28).addBox(-5, -9, -12, 2, 5, 3).texOffs(104, 28).addBox(3, -9, -12, 2, 5, 3), PartPose.offset(0, 14, -8));
            cab.addOrReplaceChild("mandibula", CubeListBuilder.create().texOffs(60, 0).addBox(-5, 0, -16, 10, 4, 16)
                    .texOffs(112, 0).addBox(-4, -3, -15, 1, 3, 1).texOffs(112, 0).addBox(3, -3, -15, 1, 3, 1)
                    .texOffs(112, 0).addBox(-1, -2, -15.5f, 1, 2, 1), PartPose.offset(0, 5, -2));
            int[][] uv = {{0, 28}, {52, 28}, {0, 54}, {52, 54}, {0, 80}};
            PartDefinition p = cab;
            for (int i = 0; i < N; i++) {
                int t = i < 4 ? 10 : 8;
                float h = t / 2f;
                p = p.addOrReplaceChild("seg" + i, CubeListBuilder.create().texOffs(uv[i][0], uv[i][1]).addBox(-h, -h, 0, t, t, 16)
                        .texOffs(104, 28).addBox(-1, -h - 4, 4, 2, 5, 3).texOffs(104, 28).addBox(-1, -h - 3, 11, 2, 4, 3),
                        PartPose.offset(0, 0, i == 0 ? 0 : 16));
            }
            p.addOrReplaceChild("cola", CubeListBuilder.create().texOffs(48, 80).addBox(-0.5f, -6, 0, 1, 12, 14), PartPose.offset(0, 0, 16));
            return LayerDefinition.create(m, 128, 128);
        }

        @Override
        public void setupAnim(Marina e, float paso, float cantidad, float edad, float yaw, float pitch) {
            cabeza.yRot = Mth.sin(edad * 0.12f + 0.8f) * 0.18f;
            cabeza.xRot = Mth.sin(edad * 0.06f) * 0.06f;
            mandibula.xRot = 0.15f + Math.max(0f, Mth.sin(edad * 0.045f)) * 0.45f;
            for (int i = 0; i <= N; i++) {
                seg[i].yRot = Mth.sin(edad * 0.12f - (i + 1) * 0.8f) * 0.32f;
                seg[i].xRot = Mth.sin(edad * 0.07f - (i + 1) * 0.6f) * 0.07f;
            }
        }

        @Override
        public void renderToBuffer(PoseStack ps, VertexConsumer vc, int luz, int overlay, float r, float g, float b, float a) {
            cabeza.render(ps, vc, luz, overlay, r, g, b, a);
        }
    }
}
