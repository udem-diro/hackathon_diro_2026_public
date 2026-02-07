package org.diro.dirosnake;

public class GameState {
    public static boolean isGameOver = false;
    public static boolean restartGame = false;

    public static void resetGameStates() {
        isGameOver = false;
        restartGame = false;
    }
}