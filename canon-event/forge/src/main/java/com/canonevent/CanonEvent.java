package com.canonevent;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import com.mojang.logging.LogUtils;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.TagParser;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;
import org.slf4j.Logger;

/** Canon Event: el mod de verdad. Los ítems del mod (con su NBT) salen en su propia pestaña del creativo. */
@Mod(CanonEvent.MODID)
public class CanonEvent {
    public static final String MODID = "canonevent";
    private static final Logger LOGGER = LogUtils.getLogger();
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    public static final RegistryObject<CreativeModeTab> PESTANA = TABS.register("canon_event", () -> CreativeModeTab.builder()
            .title(Component.literal("Canon Event"))
            .icon(CanonEvent::icono)
            .displayItems((params, output) -> {
                for (ItemStack s : itemsDelMod()) output.accept(s);
            })
            .build());

    public CanonEvent() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        TABS.register(bus);
    }

    private static ItemStack icono() {
        List<ItemStack> l = itemsDelMod();
        return l.isEmpty() ? new ItemStack(Items.BONE) : l.get(0);
    }

    /** Lee canon_creativo.txt (lo genera tools/build.py): una línea por ítem, "id_del_item|nbt". */
    static List<ItemStack> itemsDelMod() {
        List<ItemStack> out = new ArrayList<>();
        try (InputStream in = CanonEvent.class.getResourceAsStream("/canon_creativo.txt")) {
            if (in == null) return out;
            BufferedReader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8));
            String line;
            while ((line = r.readLine()) != null) {
                if (line.isBlank()) continue;
                try {
                    CompoundTag tag = new CompoundTag();
                    int bar = line.indexOf('|');
                    tag.putString("id", line.substring(0, bar));
                    tag.putByte("Count", (byte) 1);
                    String nbt = line.substring(bar + 1);
                    if (!nbt.isEmpty()) tag.put("tag", TagParser.parseTag(nbt));
                    ItemStack s = ItemStack.of(tag);
                    if (!s.isEmpty()) out.add(s);
                } catch (Exception e) {
                    LOGGER.warn("Canon Event: ítem inválido en el creativo: {}", line);
                }
            }
        } catch (Exception e) {
            LOGGER.error("Canon Event: no se pudo leer la lista del creativo", e);
        }
        return out;
    }
}
