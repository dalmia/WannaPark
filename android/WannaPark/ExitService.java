package me.org.wannapark.utils;

import android.app.IntentService;
import android.content.Intent;
import android.support.v4.content.LocalBroadcastManager;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

import me.org.wannapark.app.Config;

import static me.org.wannapark.app.Config.CLIENT_PORT1;
import static me.org.wannapark.app.Config.CLIENT_PORT2;

/**
 * Created by ADITYA on 7/1/2017.
 */
public class ExitService extends IntentService {

    String TAG = getClass().getName();

    public ExitService() {
        super("ExitService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        Log.d(TAG, "onHandleIntent");
        final int port = CLIENT_PORT2;
        ServerSocket listener = null;
        try {
            listener = new ServerSocket(port);
            listener.setReuseAddress(true);
            Log.d(TAG, String.format("listening on port = %d", port));
            Log.d(TAG, "waiting for client");
            Socket socket = listener.accept();
            Log.d(TAG, String.format("client connected from: %s", socket.getRemoteSocketAddress().toString()));
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String input = in.readLine();
            socket.close();
            Log.d(TAG, "received");
            Log.d(TAG, input);
            Intent eventIntent = new Intent("my-exit-event");
            // add data
            String data = input;
            eventIntent.putExtra("message", data);
            LocalBroadcastManager.getInstance(this).sendBroadcast(eventIntent);

        } catch (IOException e) {
            Log.d(TAG, e.toString());
        }
    }
}
