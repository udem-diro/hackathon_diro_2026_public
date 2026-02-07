open module org.diro.dirosnake {
        requires javafx.controls;
        requires javafx.fxml;
        requires javafx.media;

        requires com.almasb.fxgl.all;
        requires java.desktop;
        exports org.diro.dirosnake;
        exports org.diro.dirosnake.menu;
        exports org.diro.dirosnake.system;
}