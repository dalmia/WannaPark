package me.org.wannapark.utils;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketTimeoutException;

import me.org.wannapark.app.Config;

import static me.org.wannapark.app.Config.HOST;

/**
 * Created by ADITYA on 6/25/2017.
 */
public class SendMessage extends AsyncTask<String, Void, String> {
    private Exception exception;
    public Response response = null;

    @Override
    protected String doInBackground(String... strings) {
        try {
            try {
                Socket socket = new Socket(HOST, Integer.valueOf(strings[1]));
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(socket.getOutputStream()));
                outToServer.print(strings[0]);
                outToServer.flush();
                Log.d("yo1", strings[0]);
                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                Log.d("Out=", strings[2]);
                if(strings[2].equals("true")) {
                    String response = in.readLine();
                    Log.d("yo2", response);
                    return response;
                }

                Log.d("yo3", "Completed");
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            this.exception = e;
            return null;
        }

        return null;
    }

    @Override
    protected void onPostExecute(String s) {
        response.processFinish(s);
    }
}
