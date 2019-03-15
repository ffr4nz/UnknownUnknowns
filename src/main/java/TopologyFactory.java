import com.devo.video_recognition_storm.bolts.*;
import com.devo.video_recognition_storm.bolts.spout.ProcessVideo;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;

public class TopologyFactory {
    public static TopologyBuilder getTopology(){
        // Build A topology
        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("ProcessVideo", new ProcessVideo(), 1);
        builder.setBolt("IdentifyFaces", new IdentifyFaces(), 3)
                .shuffleGrouping("ProcessVideo");
        builder.setBolt("ExtractImages", new ExtractImages(), 3)
                .shuffleGrouping("IdentifyFaces");
        builder.setBolt("RecognizeFaces", new RecognizeFaces(), 3)
                .shuffleGrouping("ExtractImages");
        builder.setBolt("WhisperCache", new WhisperCache(), 1)
          .fieldsGrouping("RecognizeFaces", new Fields("filepath"));
        builder.setBolt("Whisper", new Whisper(), 1)
          .fieldsGrouping("WhisperCache", new Fields("filepath"));

        //       .shuffleGrouping("RecognizeFaces");
        return builder;
    }
}


/*
* TODO
*
*   - Utilizar el ticktuple para ejecutar whisper cada cierto tiempo pero no casa frame procesado
*   - Proceso en batch para entrar los desconocidos con un numero de caras minimo para que no entren en whisper en la siguiente iteracion
* */
