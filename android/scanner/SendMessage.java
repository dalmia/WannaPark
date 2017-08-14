package me.org.sampletest;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * Created by ADITYA on 6/30/2017.
 */
public class SendMessage extends AsyncTask<String, Void, Void> {
    private Exception exception;

    @Override
    protected Void doInBackground(String... strings) {
        try {
            try {
                Socket socket = new Socket("192.168.43.20", 7000);
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(socket.getOutputStream()));
                outToServer.print(strings[0]);
                outToServer.flush();
                Log.d("yo1", strings[0]);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            this.exception = e;
            return null;
        }

        return null;
    }
}

