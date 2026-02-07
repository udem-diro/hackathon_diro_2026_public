package org.diro.virusbonus;

import com.almasb.fxgl.app.GameApplication;
import com.almasb.fxgl.app.GameSettings;

public class Launcher extends GameApplication {
 
    @Override
    protected void initSettings(GameSettings settings) {
        settings.setMainMenuEnabled(true);
    }

    public static void main(String[] args) {
        launch(args);
    }
}