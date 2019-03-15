package com.devo.video_recognition_storm.bolts.spout;

import com.devo.video_recognition_storm.bolts.Constants;
import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.apache.storm.utils.Utils;

import java.io.File;
import java.io.IOException;
import java.nio.file.*;
import java.util.Map;

import static java.nio.file.StandardWatchEventKinds.ENTRY_CREATE;
import static java.nio.file.StandardWatchEventKinds.ENTRY_DELETE;
import static java.nio.file.StandardWatchEventKinds.ENTRY_MODIFY;
import static java.nio.file.StandardWatchEventKinds.OVERFLOW;

public class ProcessVideo extends BaseRichSpout {
    private SpoutOutputCollector collector;
    private long msgId = 0;
    private WatchService watcher;
    private static final Path dir = new File(Constants.VIDEOS_PATH).toPath();
    private WatchKey key;
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("filepath", "type", "size"));
    }

    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;
        try {
            watcher = FileSystems.getDefault().newWatchService();
            key = dir.register(watcher,
                    ENTRY_CREATE,
                    ENTRY_DELETE,
                    ENTRY_MODIFY);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void nextTuple() {
        Utils.sleep(100);
        try {
            for (WatchEvent<?> event: key.pollEvents()) {
                WatchEvent.Kind<?> kind = event.kind();

                // This key is registered only
                // for ENTRY_CREATE events,
                // but an OVERFLOW event can
                // occur regardless if events
                // are lost or discarded.
                // || kind == ENTRY_MODIFY
                if (kind == OVERFLOW ||
                        kind == ENTRY_DELETE ) {
                    System.out.println("No action for " + kind);
                    continue;
                }
                WatchEvent<Path> ev = (WatchEvent<Path>)event;
                Path filename = ev.context();
                System.out.println("filename " + filename.toString());
                if(filename.toString().contains("DS_Store")){
                    continue;
                }
                Path child = dir.resolve(filename);
                System.out.println(child.toString());
                System.out.println(Files.probeContentType(child));

                File fileTmp = new File(child.toAbsolutePath().toString());
                collector.emit(new Values(child.toAbsolutePath().toString(),
                        "video", fileTmp.length()),
                        ++msgId);

            }
        } catch (IOException x) {
            System.err.println(x);
        }
//        boolean valid = key.reset();
//        if (!valid) {
//            System.err.format("No reset on file ...");
//        }
    }

    @Override
    public void ack(Object msgId) {
        System.out.println("Got ACK for msgId : " + msgId);
    }

    @Override
    public void fail(Object msgId) {
        System.out.println("Got FAIL for msgId : " + msgId);
    }

}
