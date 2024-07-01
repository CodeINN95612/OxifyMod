package com.codinn.oxify.item.custom;

import java.util.Optional;

import org.jetbrains.annotations.Nullable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.codinn.oxify.Oxify;

import net.minecraft.advancement.criterion.Criteria;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.Oxidizable;
import net.minecraft.block.OxidizableBlock;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.item.ItemUsageContext;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.util.ActionResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.world.WorldEvents;
import net.minecraft.world.event.GameEvent;

public class OxidizerItem extends Item {

    public OxidizerItem(Settings settings) {
        super(settings);
    }

    @Override
    public boolean isEnchantable(ItemStack stack) {
        return false;
    }
    
    @Override
    public ActionResult useOnBlock(ItemUsageContext context) {
        World world = context.getWorld();
        BlockPos blockPosition = context.getBlockPos();
        PlayerEntity player = context.getPlayer();
        BlockState blockState = world.getBlockState(blockPosition);

        Optional<BlockState> degradationState = tryDegrade(world, blockPosition, player, blockState);

        if (!degradationState.isPresent()) {
            return ActionResult.PASS;
        }

        ItemStack itemStack = context.getStack();
        if (player instanceof ServerPlayerEntity serverPlayer) {
            Criteria.ITEM_USED_ON_BLOCK.trigger(serverPlayer, blockPosition, itemStack);
        }

        world.setBlockState(blockPosition, degradationState.get(), Block.NOTIFY_ALL_AND_REDRAW);
        world.emitGameEvent(GameEvent.BLOCK_CHANGE, blockPosition, GameEvent.Emitter.of(player, degradationState.get()));

        if (player != null) {
            itemStack.damage(1, player, LivingEntity.getSlotForHand(context.getHand()));
        }

        return ActionResult.success(world.isClient);
    }

    private Optional<BlockState> tryDegrade(World world, BlockPos pos, @Nullable PlayerEntity player, BlockState state) {
        if (state.getBlock() instanceof OxidizableBlock block) {
            Optional<BlockState> degradedState = block.getDegradationResult(state);
            world.playSound(player, pos, SoundEvents.ITEM_AXE_SCRAPE, SoundCategory.BLOCKS, 1.0F, 1.0F);
            world.syncWorldEvent(player, WorldEvents.BLOCK_SCRAPED, pos, 0);
            return degradedState;
        }

        return Optional.empty();
    }
}
