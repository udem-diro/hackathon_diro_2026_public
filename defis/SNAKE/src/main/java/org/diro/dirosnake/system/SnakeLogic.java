package org.diro.dirosnake.system;

import com.almasb.fxgl.dsl.FXGL;
import com.almasb.fxgl.entity.Entity;
import com.almasb.fxgl.entity.components.CollidableComponent;
import javafx.scene.shape.Rectangle;
import org.diro.dirosnake.Constants;
import org.diro.dirosnake.Directions;
import org.diro.dirosnake.EntityTypes;

import java.util.ArrayList;

public class SnakeLogic {

    /** [NOTE DU D.I.R.O.]
     * Puisque la variable "snake" est un ArrayList, les éléments sont passés par référence (pas exactement mais on peut
     * assumer que oui pour la suite du développement), ils sont donc modifiés directement dans les fonctions lorsque
     * la variable est passé en argument. Pour plus d'information, cliquer sur le lien suivant:
     * https://stackoverflow.com/questions/40480/is-java-pass-by-reference-or-pass-by-value?page=1&tab=scoredesc#tab-top
     */

    public static void expendSnake(ArrayList<SnakeCell> snake) {
        //TODO: Coder la fonction pour élargir le S.N.A.K.E. ici.
    }

    public static void moveSnake(ArrayList<SnakeCell> snake, Directions direction) {
        //TODO: Coder la fonction pour faire avancer le S.N.A.K.E. ici.

        /* [NOTE DU D.I.R.O.]
         * Ne pas oublier que chaque cellule du S.N.A.K.E. doit mettre à jour la direction.
         * Cella sera utile lorsqu'il faudra faire la fonction "expendSnake" et faire avancer
         * le S.N.A.K.E. automatiquement selon la direction à laquelle il fait face.
         */
    }

    private static void snakeCollidesBody(ArrayList<SnakeCell> snake) {
        //TODO: Coder la détection des collisions entre le corps du S.N.A.K.E. et sa tête ici.
    }

    private static void snakeCollidesScreenEdges(ArrayList<SnakeCell> snake) {
        //TODO: Coder la détection des collisions avec les côtés de l'écran ici.
    }

    public static void spawnData(ArrayList<SnakeCell> snake) {
        //TODO: Coder l'apparition des données ici.
    }

    public static void initGame(ArrayList<SnakeCell> snake) {
        Entity head = FXGL.entityBuilder()
                .type(EntityTypes.HEAD)
                .at(Constants.GRID_SCALE * 5, Constants.GRID_SCALE * 8)
                .viewWithBBox(new Rectangle(Constants.GRID_SCALE, Constants.GRID_SCALE, Constants.SNAKE_HEAD_COLOR))
                .with(new CollidableComponent(true))
                .buildAndAttach();

        snake.add(new SnakeCell(head, Directions.RIGHT));
    }
}