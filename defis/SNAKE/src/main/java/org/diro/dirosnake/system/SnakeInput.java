package org.diro.dirosnake.system;

import com.almasb.fxgl.input.Input;

import java.util.ArrayList;

public class SnakeInput {

    // Member variables
    private final Input inputManager;
    private final ArrayList<SnakeCell> snake;

    public SnakeInput(ArrayList<SnakeCell> snake, Input inputManager) {
        this.inputManager = inputManager;
        this.snake = snake;
    }

    public void init() {
        inputHandler();
    }

    private void inputHandler() {
        //TODO: Ajouter la capacité de faire bouger le S.N.A.K.E. avec les touches du clavier ici.
    }
}