import com.devo.video_recognition_storm.bolts.Constants;
import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.utils.Utils;

// Show more examples in
// https://github.com/apache/storm/tree/v1.1.2/examples/storm-starter

public class StartLocalCluster {
    private static final int SLEEP_MILLIS = 200;
    private static boolean isAlive = true;
    public static void main(String[] args){
        Config conf = new Config();
        // Uncomment this line to show debug information.
        // conf.setDebug(true);
        conf.setNumWorkers(Constants.NUMBER_OF_WORKERS_AT_START);

        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try {
                    Thread.sleep(SLEEP_MILLIS);
                    System.out.println("Shouting down ...");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                isAlive = false;
            }
        });
        LocalCluster cluster = new LocalCluster();
        TopologyBuilder tb = TopologyFactory.getTopology();
        cluster.submitTopology("video_processing", conf, tb.createTopology());
        while (isAlive){
            // Do nothing. Wait for shutdown signal.
            // This is only for local testing.
        }

        cluster.killTopology("video_processing");
        cluster.shutdown();
    }
}
