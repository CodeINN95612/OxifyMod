package com.codinn.oxify;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroupEntries;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.enchantment.Enchantment;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemGroups;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.registry.tag.TagKey;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Oxify implements ModInitializer {
	public static final String MOD_ID = "oxify";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static final TagKey<Enchantment> OXIDIZER_ENCHANTMENTS_TAG = TagKey.of(
		RegistryKeys.ENCHANTMENT, 
		Identifier.of(MOD_ID, "oxidizer_enchantments"));
	
	public static final ItemGroup OXIFY_GROUP = registerItemGroup(
		"oxify",  
		FabricItemGroup
			.builder()
			.displayName(Text.translatable("oxify.item_group_name"))
			.icon(() -> new ItemStack(OxifyItems.OXIDIZER))
			.entries((displayContext, entries) -> {
				entries.add(OxifyItems.OXIDIZER);
				entries.add(Items.AMETHYST_SHARD);
				entries.add(Items.COPPER_INGOT);
				entries.add(Items.STICK);
			})
			.build());

	@Override
	public void onInitialize() {
		registerItems();
	}

	private static void registerItems() {
		LOGGER.info("Registering items");
		OxifyItems.initialize();
		ItemGroupEvents
			.modifyEntriesEvent(ItemGroups.TOOLS)
			.register(Oxify::addItemsToGroup);
	}

	private static ItemGroup registerItemGroup(String path, ItemGroup group) {
		Identifier id = Identifier.of(MOD_ID, path);
		LOGGER.info("Registering item group: " + path + " with id: " + id.toString());
		return Registry.register(Registries.ITEM_GROUP, id, group);
	}

	private static void addItemsToGroup(FabricItemGroupEntries entries){
		entries.add(OxifyItems.OXIDIZER);
	}
}