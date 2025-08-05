package com.codinn.oxify;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.codinn.oxify.item.custom.OxidizerItem;

import net.minecraft.item.Item;
import net.minecraft.item.Items;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.util.Identifier;
import java.util.function.Function;

public final class OxifyItems {

    public static final Logger LOGGER = LoggerFactory.getLogger(Oxify.MOD_ID);
    
    public OxifyItems() {}

    public static void initialize() {
    }

    public static final Item OXIDIZER = register(
		"oxidizer", 
		OxidizerItem::new,
        new Item.Settings()
            .maxDamage(64));

    public static Item register(String path, Function<Item.Settings, Item> factory, Item.Settings settings) {
        
        Identifier id = Identifier.of(Oxify.MOD_ID, path);
        LOGGER.info("Registering item: " + path + " with id: " + id.toString());
        final RegistryKey<Item> registryKey = RegistryKey.of(RegistryKeys.ITEM, id);
        return Items.register(registryKey, factory, settings);
    }
}
