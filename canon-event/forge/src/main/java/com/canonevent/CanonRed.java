package com.canonevent;

import java.util.function.Supplier;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.DistExecutor;
import net.minecraftforge.network.NetworkEvent;
import net.minecraftforge.network.NetworkRegistry;
import net.minecraftforge.network.simple.SimpleChannel;

/** Red del mod: el servidor le cuenta a cada jugador su miedo, quién lo acecha y si lo persiguen. */
public class CanonRed {
    private static final String V = "1";
    public static final SimpleChannel CANAL = NetworkRegistry.newSimpleChannel(new ResourceLocation(CanonEvent.MODID, "main"),
            () -> V, s -> true, s -> true);

    public static void registrar() {
        CANAL.registerMessage(0, Estado.class, Estado::escribir, Estado::leer, Estado::manejar);
    }

    /** miedo 0..100; acechador = nombre de quien te mira ("" si nadie); visto = te tiene a la vista; persecucion = algo te persigue. */
    public record Estado(int miedo, String acechador, boolean visto, boolean persecucion, float distancia) {
        void escribir(FriendlyByteBuf b) {
            b.writeVarInt(miedo);
            b.writeUtf(acechador, 64);
            b.writeBoolean(visto);
            b.writeBoolean(persecucion);
            b.writeFloat(distancia);
        }

        static Estado leer(FriendlyByteBuf b) {
            return new Estado(b.readVarInt(), b.readUtf(64), b.readBoolean(), b.readBoolean(), b.readFloat());
        }

        void manejar(Supplier<NetworkEvent.Context> ctx) {
            ctx.get().enqueueWork(() -> DistExecutor.unsafeRunWhenOn(Dist.CLIENT, () -> () -> CanonCliente.recibir(this)));
            ctx.get().setPacketHandled(true);
        }
    }
}
