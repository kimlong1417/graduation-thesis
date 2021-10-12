import org.graalvm.compiler.phases.common.NodeCounterPhase.Stage;
import org.hibernate.SessionFactory;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import utils.HibernateUtils;
import utils.StageHelper;

public class App extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(final Stage primaryStage) {
        try {
            SessionFactory factory = HibernateUtils.getSessionFactory();
            Parent root = FXMLLoader.load(getClass().getClassLoader().getResource("demo.fxml"));
            StageHelper.startStage(root);
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
