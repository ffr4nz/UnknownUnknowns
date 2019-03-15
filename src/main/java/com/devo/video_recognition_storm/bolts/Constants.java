package com.devo.video_recognition_storm.bolts;

public class Constants {

    final static String DIR = System.getProperty("user.dir");

    // You can use a absolute path like
    //  final static String SCRIPTS_PATH = "/path/to/Python/scripts";
    public static final String SCRIPTS_PATH = DIR +
            "/src/main/resources/";
    public static final String VIDEOS_PATH = "/opt/face-recognition/videos";
    public static final int NUMBER_OF_WORKERS_AT_START = 2;
    static {
      System.out.println("----------- DIR PATH ---------------");
      System.out.println(DIR);
      System.out.println("----------- DIR PATH ---------------");
    }
}
