package com.devo.video_recognition_storm.bolts;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

import java.util.Map;

public class ExtractImages extends ShellBolt implements IRichBolt {
    public ExtractImages() {
        super("python3", Constants.SCRIPTS_PATH + "ExtractImages.py");
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("filepath", "output_image",
                "encoding", "boxes", "r"));
    }

    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
