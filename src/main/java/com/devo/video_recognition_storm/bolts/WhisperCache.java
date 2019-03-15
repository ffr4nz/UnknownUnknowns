package com.devo.video_recognition_storm.bolts;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;
import org.apache.storm.Config;
import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;


public class WhisperCache  extends BaseBasicBolt {


  public static final String SYSTEM_COMPONENT_ID = "__system";
  public static final String SYSTEM_TICK_STREAM_ID = "__tick";

  //Create logger for this class
  private static final Logger logger = LogManager.getLogger(WhisperCache.class);

  private static final int EMIT_FREQUENCY = 3;
  private static Map<String,Long> lastEvents = new ConcurrentHashMap<>();
  //For holding words and counts
  private Map<String, List<Tuple>> eventsRecived = new ConcurrentHashMap<>();

  //How often to emit a count of words
  private Integer emitFrequency;

  public WhisperCache(){
    emitFrequency = EMIT_FREQUENCY;
  }

  public WhisperCache(int emitFrequency){
    this.emitFrequency = emitFrequency;
  }

  //Configure frequency of tick tuples for this bolt
  //This delivers a 'tick' tuple on a specific interval,
  //which is used to trigger certain actions
  @Override
  public Map<String, Object> getComponentConfiguration() {
    Config conf = new Config();
    conf.put(Config.TOPOLOGY_TICK_TUPLE_FREQ_SECS, emitFrequency);
    return conf;
  }

  //execute is called to process tuples
  @Override
  public void execute(Tuple tuple, BasicOutputCollector collector) {
    //If it's a tick tuple, emit all words and counts
    long now = new Date().getTime();
    if(isTickTuple(tuple)) {
      logger.info("--------------> lastEvents: " + lastEvents.toString());
      logger.info("--------------> eventsRecived: "
        + eventsRecived.values().size());
      for (String key : lastEvents.keySet()) {
        Long lastEvent = lastEvents.get(key);
        if (now - lastEvent>15000){
          List<Tuple> listOfTuplesToSend = eventsRecived.get(key);
          if(listOfTuplesToSend != null){
            for(Tuple tupleToSend: listOfTuplesToSend){
              collector.emit(new Values("OI","Alias",tupleToSend.getString(2)));
              // In this code you can made things with the tuples.
              break;
            }

            eventsRecived.remove(key);
            lastEvents.remove(key);
          }
        }
      }
    } else {
      //Get the filepath
      String filepath = tuple.getString(2);
      if(eventsRecived.containsKey(filepath)){
        eventsRecived.get(filepath).add(tuple);
      }else{
        ArrayList<Tuple> listOfTuples = new ArrayList<Tuple>();
        listOfTuples.add(tuple);
        eventsRecived.put(filepath, listOfTuples);
      }
      lastEvents.put(filepath,now);

    }
  }


  //Declare that this emits a tuple containing two fields; word and count
  @Override
  public void declareOutputFields(OutputFieldsDeclarer declarer) {
    declarer.declare(new Fields("image_path", "alias", "filepath"));
  }

  public static boolean isTickTuple(Tuple tuple) {
    return tuple.getSourceComponent().equals(SYSTEM_COMPONENT_ID)
      && tuple.getSourceStreamId().equals(SYSTEM_TICK_STREAM_ID);
  }

}
