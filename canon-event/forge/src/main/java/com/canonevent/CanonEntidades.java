package com.canonevent;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

/** Entidades propias del mod (Java): summon canonevent:diana / canonevent:gigante */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class CanonEntidades {
    public static final DeferredRegister<EntityType<?>> ENT = DeferredRegister.create(Registries.ENTITY_TYPE, CanonEvent.MODID);

    public static final RegistryObject<EntityType<Monstruo>> DIANA = ENT.register("diana", () -> EntityType.Builder
            .<Monstruo>of((t, l) -> new Monstruo(t, l, Monstruo.Tipo.DIANA), MobCategory.MONSTER)
            .sized(0.7f, 3.0f).clientTrackingRange(12).build("canonevent:diana"));

    public static final RegistryObject<EntityType<Monstruo>> GIGANTE = ENT.register("gigante", () -> EntityType.Builder
            .<Monstruo>of((t, l) -> new Monstruo(t, l, Monstruo.Tipo.GIGANTE), MobCategory.MONSTER)
            .sized(2.6f, 12.0f).clientTrackingRange(24).build("canonevent:gigante"));

    @SubscribeEvent
    public static void atributos(EntityAttributeCreationEvent e) {
        e.put(DIANA.get(), Monstruo.atributosDiana().build());
        e.put(GIGANTE.get(), Monstruo.atributosGigante().build());
    }
}
