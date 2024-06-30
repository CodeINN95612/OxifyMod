package com.codinn.oxify;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.fabricmc.api.ClientModInitializer;

public class OxifyClient implements ClientModInitializer {
    public static final Logger LOGGER = LoggerFactory.getLogger(Oxify.MOD_ID);
    
    @Override
    public void onInitializeClient() {
        LOGGER.info("Hello Fabric world client!");

    }
    
}
