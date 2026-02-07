package org.diro.dirosnake.system;

import com.almasb.fxgl.physics.PhysicsWorld;


import java.util.ArrayList;

public class SnakePhysics {

    // Member variables
    private final PhysicsWorld physicsWorld;
    private final ArrayList<SnakeCell> snake;

    public SnakePhysics(ArrayList<SnakeCell> snake, PhysicsWorld physicsWorld) {
        this.physicsWorld = physicsWorld;
        this.snake = snake;
    }

    public void init() {
        collisionHandler();
    }

    private void collisionHandler() {
        //TODO: Coder la détection des collisions avec les données ici.

        // [NOTE DU D.I.R.O.]
        // Bien que possible, vous ne devez pas faire la détection des collisions entre le
        // S.N.A.K.E. et son corps ou les côtés de l'écran ici.
    }
}