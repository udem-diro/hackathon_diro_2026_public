package org.diro.dirosnake.system;

import com.almasb.fxgl.entity.Entity;
import org.diro.dirosnake.Directions;

/** [NOTE DU D.I.R.O.]
 * Ce qui compose le S.N.A.K.E.
 * Cette classe est composé d'une entité (Vous pouvez voir les entités comme les objets qui seront affiché dans la scène)
 * ainsi que d'une direction qui est simplement un énumérateur définit dans la classe "Directions".
 */
public class SnakeCell {
    public Directions direction;
    private Entity entity;

    SnakeCell(Entity entity, Directions direction) {
        this.entity = entity;
        this.direction = direction;
    }

    public Entity getEntity() {
        return this.entity;
    }
}