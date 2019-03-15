package com.devo.video_recognition_storm.bolts;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;

import java.util.Map;

public class RecognizeFaces extends ShellBolt implements IRichBolt {
    public RecognizeFaces() {
        super("python3", Constants.SCRIPTS_PATH + "RecognizeFaces.py");
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("image_path", "alias", "filepath"));
    }

    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
