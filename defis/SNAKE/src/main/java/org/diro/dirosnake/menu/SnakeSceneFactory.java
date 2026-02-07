package org.diro.dirosnake.menu;

import com.almasb.fxgl.app.scene.*;

public class SnakeSceneFactory extends SceneFactory {

    @Override
    public FXGLMenu newMainMenu() {
        // TODO: Remplacer le FXGLDefaultMenu par MainMenu pour voir votre menu personnalisé.
        return new FXGLDefaultMenu(MenuType.MAIN_MENU);
    }

    @Override
    public FXGLMenu newGameMenu() {
        return new GameOverMenu();
    }
}