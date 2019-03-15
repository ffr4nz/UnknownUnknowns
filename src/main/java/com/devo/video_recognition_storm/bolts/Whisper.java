package com.devo.video_recognition_storm.bolts;

import org.apache.storm.task.ShellBolt;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;

import java.util.Map;

public class Whisper extends ShellBolt implements IRichBolt {
    public Whisper() {
        super("python3", Constants.SCRIPTS_PATH + "Whisper.py");
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    }

    public Map<String, Object> getComponentConfiguration() {
        return null;
    }
}
