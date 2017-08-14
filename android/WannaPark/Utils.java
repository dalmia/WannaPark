package me.org.wannapark.utils;

import android.content.Context;

/**
 * Created by ADITYA on 6/29/2017.
 */
public class Utils {
    public static void makeRequest(String message, String port, Response response, boolean ret){
        SendMessage msg = new SendMessage();
        msg.response = response;
        msg.execute(message, port, String.valueOf(ret));
    }
}
