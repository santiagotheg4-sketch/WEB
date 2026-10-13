package com.canonevent;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

/** Entidades propias del mod (Java): summon canonevent:diana / gigante / masa / ahogada / leviatan */
@Mod.EventBusSubscriber(modid = CanonEvent.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class CanonEntidades {
    public static final DeferredRegister<EntityType<?>> ENT = DeferredRegister.create(Registries.ENTITY_TYPE, CanonEvent.MODID);

    public static final RegistryObject<EntityType<Monstruo>> DIANA = ENT.register("diana", () -> EntityType.Builder
            .<Monstruo>of((t, l) -> new Monstruo(t, l, Monstruo.Tipo.DIANA), MobCategory.MONSTER)
            .sized(0.7f, 3.0f).clientTrackingRange(12).build("canonevent:diana"));

    public static final RegistryObject<EntityType<Monstruo>> GIGANTE = ENT.register("gigante", () -> EntityType.Builder
            .<Monstruo>of((t, l) -> new Monstruo(t, l, Monstruo.Tipo.GIGANTE), MobCategory.MONSTER)
            .sized(2.6f, 12.0f).clientTrackingRange(24).build("canonevent:gigante"));

    public static final RegistryObject<EntityType<Masa>> MASA = ENT.register("masa", () -> EntityType.Builder
            .<Masa>of(Masa::new, MobCategory.MONSTER)
            .sized(0.95f, 2.9f).clientTrackingRange(10).build("canonevent:masa"));

    public static final RegistryObject<EntityType<Marina>> AHOGADA = ENT.register("ahogada", () -> EntityType.Builder
            .<Marina>of((t, l) -> new Marina(t, l, Marina.Tipo.AHOGADA), MobCategory.MONSTER)
            .sized(0.6f, 1.9f).clientTrackingRange(10).build("canonevent:ahogada"));

    public static final RegistryObject<EntityType<Marina>> LEVIATAN = ENT.register("leviatan", () -> EntityType.Builder
            .<Marina>of((t, l) -> new Marina(t, l, Marina.Tipo.LEVIATAN), MobCategory.MONSTER)
            .sized(3.0f, 2.5f).clientTrackingRange(16).build("canonevent:leviatan"));

    public static final RegistryObject<EntityType<Nicolas>> NICOLAS = ENT.register("nicolas", () -> EntityType.Builder
            .<Nicolas>of(Nicolas::new, MobCategory.MONSTER).sized(0.6f, 1.95f).clientTrackingRange(8).build("canonevent:nicolas"));

    @SubscribeEvent
    public static void atributos(EntityAttributeCreationEvent e) {
        e.put(DIANA.get(), Monstruo.atributosDiana().build());
        e.put(GIGANTE.get(), Monstruo.atributosGigante().build());
        e.put(MASA.get(), Masa.atributos().build());
        e.put(AHOGADA.get(), Marina.atributosAhogada().build());
        e.put(LEVIATAN.get(), Marina.atributosLeviatan().build());
        e.put(NICOLAS.get(), Nicolas.atributos().build());
    }
}
