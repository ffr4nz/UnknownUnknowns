package com.devo.video_recognition_storm.bolts;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

import java.util.Map;

public class IdentifyFaces extends ShellBolt implements IRichBolt {
    public IdentifyFaces() {
        super("python3", Constants.SCRIPTS_PATH + "IdentifyFaces.py");
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("filepath", "output_image", "type"));
    }

    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
