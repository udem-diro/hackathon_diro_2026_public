package org.diro.dirosnake;

import com.almasb.fxgl.dsl.FXGL;

public class TimeHelper {

    private static double startTime = 0;

    public static void resetTime() {
        startTime = FXGL.getGameTimer().getNow();
    }

    public static double getStartTime() {
        return startTime;
    }
}