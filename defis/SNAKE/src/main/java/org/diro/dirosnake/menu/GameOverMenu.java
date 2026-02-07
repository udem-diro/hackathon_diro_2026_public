package org.diro.dirosnake.menu;

import com.almasb.fxgl.animation.Animation;
import com.almasb.fxgl.animation.Interpolators;
import com.almasb.fxgl.app.scene.FXGLMenu;
import com.almasb.fxgl.app.scene.MenuType;
import com.almasb.fxgl.core.util.EmptyRunnable;
import com.almasb.fxgl.dsl.FXGL;
import javafx.geometry.Point2D;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Text;
import javafx.util.Duration;
import org.diro.dirosnake.Constants;
import org.diro.dirosnake.GameState;

/** [NOTE DU D.I.R.O.]
 * Vous pouvez utiliser cette classe comme référence pour faire le menu principal.
 * Il est possible d'activer le menu en appuyant sur "ESC" après avoir lancé une nouvelle partie.
 */
public class GameOverMenu extends FXGLMenu {

    private Animation<?> menuAnimation;
    private Animation<?> resumeAnimation;
    private Animation<?> exitAnimation;
    private Animation<?> restartAnimation;
    Button resumeButton;
    Button exitButton;
    Button restartButton;
    Text gameOverTitle;
    private boolean gameOverFlag = false;

    public GameOverMenu() {
        super(MenuType.GAME_MENU);
        String transparentProperty = "-fx-background-color: transparent;";

        Node background = createBackground();

        // GAME OVER TITLE
        gameOverTitle = FXGL.getUIFactoryService().newText("GAME OVER");
        gameOverTitle.setTranslateY((double)Constants.HEIGHT/4);
        gameOverTitle.setScaleX(6);
        gameOverTitle.setScaleY(6);

        // RESUME BUTTON
        resumeButton = FXGL.getUIFactoryService().newButton("RESUME");
        resumeButton.setStyle(transparentProperty);
        resumeButton.setTranslateY((double)Constants.HEIGHT/4);
        resumeButton.setFocusTraversable(false);
        resumeButton.setScaleX(6);
        resumeButton.setScaleY(6);
        resumeButton.setOnMouseEntered( event -> {
            resumeAnimation.start();
            FXGL.play("codecopen.wav");
        });
        resumeButton.setOnMouseExited( event -> {
            resumeButton.setOpacity(1.0);
            resumeAnimation.stop();
        });
        resumeButton.setOnMouseClicked(event -> {
            FXGL.getGameController().gotoPlay();
            FXGL.play("codecover.wav");
        });

        // EXIT TO MAIN MENU BUTTON
        exitButton = FXGL.getUIFactoryService().newButton("MAIN MENU");
        exitButton.setCenterShape(true);
        exitButton.setStyle(transparentProperty);
        exitButton.setTranslateY((double)Constants.HEIGHT/2);
        exitButton.setFocusTraversable(false);
        exitButton.setScaleX(2);
        exitButton.setScaleY(2);
        exitButton.setOnMouseEntered( event -> {
            exitAnimation.start();
            FXGL.play("codecopen.wav");
        });
        exitButton.setOnMouseExited( event -> {
            exitButton.setOpacity(1.0);
            exitAnimation.stop();
        });
        exitButton.setOnMouseClicked(event -> {
            GameState.restartGame = true;
            FXGL.getGameController().gotoMainMenu();
            FXGL.play("exit.wav");
        });

        // RESTART BUTTON
        restartButton = FXGL.getUIFactoryService().newButton("RESTART");
        restartButton.setStyle(transparentProperty);
        restartButton.setTranslateY((double)Constants.HEIGHT/2);
        restartButton.setFocusTraversable(false);
        restartButton.setScaleX(2);
        restartButton.setScaleY(2);
        restartButton.setOnMouseEntered( event -> {
            restartAnimation.start();
            FXGL.play("codecopen.wav");
        });
        restartButton.setOnMouseExited( event -> {
            restartButton.setOpacity(1.0);
            restartAnimation.stop();
        });
        restartButton.setOnMouseClicked(event -> {
            GameState.restartGame = true;
            FXGL.getGameController().gotoPlay();
            FXGL.play("found.wav");
        });

        // ADD NODES TO THE SCENE
        getContentRoot().getChildren().addAll(background, gameOverTitle, resumeButton, exitButton, restartButton);

        // ANIMATIONS
        resumeAnimation = createTextAnimation(resumeButton);
        exitAnimation = createTextAnimation(exitButton);
        restartAnimation = createTextAnimation(restartButton);
        menuAnimation = FXGL.animationBuilder()
                .duration(Duration.seconds(0.66))
                .interpolator(Interpolators.EXPONENTIAL.EASE_OUT())
                .scale(getContentRoot())
                .from(new Point2D(0, 0))
                .to(new Point2D(1, 1))
                .build();
    }

    private Node createBackground() {
        Rectangle bg = new Rectangle(Constants.WIDTH, Constants.HEIGHT);
        bg.setFill(new Color(0.,0.,0.,0.8));
        return bg;
    }

    private void hideNode(Node node) {
        node.setVisible(false);
        node.setManaged(false);
    }

    private void showNode(Node node) {
        node.setVisible(true);
        node.setManaged(true);
    }

    private Animation<?> createTextAnimation(Button button) {
        return FXGL.animationBuilder()
                .duration(Duration.seconds(0.95))
                .interpolator(Interpolators.SMOOTH.EASE_IN_OUT())
                .repeatInfinitely()
                .autoReverse(true)
                .animate(button.opacityProperty())
                .from(1)
                .to(0.5)
                .build();
    }

    @Override
    public void onCreate() {
        menuAnimation.setOnFinished(EmptyRunnable.INSTANCE);
        menuAnimation.stop();
        menuAnimation.start();
    }

    @Override
    protected void onUpdate(double tpf) {
        menuAnimation.onUpdate(tpf);
        resumeAnimation.onUpdate(tpf);
        restartAnimation.onUpdate(tpf);
        exitAnimation.onUpdate(tpf);

        gameOverTitle.setTranslateX((double)Constants.WIDTH/2 - gameOverTitle.getBoundsInLocal().getWidth()/2);
        resumeButton.setTranslateX((double)Constants.WIDTH/2 - resumeButton.getWidth()/2);
        exitButton.setTranslateX((double)Constants.WIDTH/1.25 - exitButton.getWidth()/2 );
        restartButton.setTranslateX((double)Constants.WIDTH/4 - restartButton.getWidth()/2);

        if (GameState.isGameOver && !gameOverFlag) {
            hideNode(resumeButton);
            showNode(gameOverTitle);
            gameOverFlag = true;
        }

        else if (!GameState.isGameOver) {
            hideNode(gameOverTitle);
            showNode(resumeButton);
            gameOverFlag = false;
        }
    }
}