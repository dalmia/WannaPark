package me.org.wannapark;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.widget.CardView;
import android.text.format.Formatter;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Calendar;
import java.util.TimeZone;

import me.org.wannapark.app.Config;
import me.org.wannapark.utils.ExitService;
import me.org.wannapark.utils.QRService;
import me.org.wannapark.utils.Response;
import me.org.wannapark.utils.Utils;

import static me.org.wannapark.app.Config.CLIENT_PORT2;
import static me.org.wannapark.app.Config.KEY_COST;
import static me.org.wannapark.app.Config.KEY_HOURS;
import static me.org.wannapark.app.Config.KEY_MINUTES;
import static me.org.wannapark.app.Config.KEY_PARKING_SPOT;
import static me.org.wannapark.app.Config.KEY_PORT;
import static me.org.wannapark.app.Config.KEY_SECONDS;
import static me.org.wannapark.app.Config.KEY_TIME;

public class IndoorActivity extends Activity implements Response, SensorEventListener{

    TextView textViewParkingSpot;
    TextView textViewParkingTime;
    TextView navigation;
    ImageView imageViewNavigation;
    CardView navigationView;


    ProgressDialog pDialog;
    String parkingSpot;
    String time;
    int hours;
    int minutes;
    int seconds;
    SensorManager sensorManager;
    long timeStart = -1;
    int pos = 0;
    float threshold = 500;
    long timeLast;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_indoor);
        textViewParkingSpot = (TextView) findViewById(R.id.parkSpot);
        textViewParkingTime = (TextView) findViewById(R.id.parkTime);
        navigation = (TextView) findViewById(R.id.navigation);
        navigationView = (CardView) findViewById(R.id.navigationView);
        imageViewNavigation = (ImageView) findViewById(R.id.internalNav);
        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        Sensor light = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
        sensorManager.registerListener(this, light, SensorManager.SENSOR_DELAY_FASTEST);

        Intent intent = getIntent();
        parkingSpot = intent.getStringExtra(KEY_PARKING_SPOT);
        time = intent.getStringExtra(KEY_TIME);
        hours = intent.getIntExtra(KEY_HOURS, 0);
        minutes = intent.getIntExtra(KEY_MINUTES, 0);
        seconds = intent.getIntExtra(KEY_SECONDS, 0);

        textViewParkingSpot.setText("Parking Spot: " + parkingSpot);
        textViewParkingTime.setText("Entry Time: " + time);

        switch (parkingSpot) {
            case "1":
                imageViewNavigation.setImageResource(R.drawable.route1);
                break;
            case "2":
                imageViewNavigation.setImageResource(R.drawable.route2);
                break;
            case "3":
                imageViewNavigation.setImageResource(R.drawable.route3);
                break;
            case "4":
                imageViewNavigation.setImageResource(R.drawable.route4);
                break;
            case "5":
                imageViewNavigation.setImageResource(R.drawable.route5);
                break;
            case "6":
                imageViewNavigation.setImageResource(R.drawable.route6);
                break;
            case "7":
                imageViewNavigation.setImageResource(R.drawable.route7);
                break;
            case "8":
                imageViewNavigation.setImageResource(R.drawable.route8);
                break;
        }
//        this.startService(new Intent(this, QRService.class));
    }

    @Override
    public void onBackPressed() {

    }

    public void exitClick(View view) {

        SharedPreferences prefs = getSharedPreferences(Config.KEY_PREF_NAME, MODE_PRIVATE);
        String sessionKey = prefs.getString("key", null);
        if (sessionKey != null) {
//            this.startService(new Intent(this, ExitService.class));
            pDialog = new ProgressDialog(this);
            pDialog.setMessage("Verifying identity...");
            pDialog.setCancelable(false);
            pDialog.show();

            WifiManager wm = (WifiManager) getSystemService(WIFI_SERVICE);
            String ip = Formatter.formatIpAddress(wm.getConnectionInfo().getIpAddress());
            String message = "TAKE_EXIT_IMAGE::" + sessionKey + "::" + ip + "::" + CLIENT_PORT2;
            Utils.makeRequest(message,String.valueOf(Config.PORT3) , this, true);
        }
    }

    @Override
    public void processFinish(String output) {
        if(output == null) return;
        pDialog.cancel();

        if(output.equals("SECURITY_PASSED")) {

            Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("GMT+5:30"));
            int secondsExit = calendar.get(Calendar.SECOND);
            int minutesExit = calendar.get(Calendar.MINUTE);
            int hours_exit = calendar.get(Calendar.HOUR);

            int diffHr = hours_exit - hours;
            int diffMin = minutesExit - minutes;
            int diffSec = secondsExit - seconds;

            if (diffHr < 0) {
                diffHr = diffHr + 12;
            }
            if (diffMin < 0) {
                diffMin = diffMin + 60;
            }
            if (diffSec < 0) {
                diffSec = diffSec + 60;
            }

            int totSecs = diffSec + (diffMin * 60) + (diffHr * 60 * 60);
            int cost = totSecs * 50;

            Intent intent = new Intent(this, ExitActivity.class);
            intent.putExtra(KEY_HOURS, diffHr);
            intent.putExtra(KEY_MINUTES, diffMin);
            intent.putExtra(KEY_SECONDS, diffSec);
            intent.putExtra(KEY_COST, cost);
            startActivity(intent);
        }else{
            Toast.makeText(IndoorActivity.this, "Security Verification Failed !!", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        int thValue = 1;
        float value = sensorEvent.values[0];
        if (value < threshold) thValue = 0;
//        Log.d("Yo", String.valueOf(value) + ":" + thValue);
        if (thValue == 1) {
            timeLast = Calendar.getInstance().getTimeInMillis();
            if (timeStart == -1) timeStart = timeLast;
        } else {
            if (timeStart != -1) {
                long timeElapsed = (timeLast - timeStart);
                if(pos == 0 && timeElapsed > threshold){
                    Toast.makeText(IndoorActivity.this, "Li-fi detected", Toast.LENGTH_SHORT).show();
                    String text;
                    switch (parkingSpot){
                        case "1": text = "Go Left. You have reached your destination.";
                            break;
                        case "2": text = "Go Straight and take a left. You have reached your destination.";
                            break;
                        case "5": text = "Go Right. You have reached your destination.";
                            break;
                        case "6": text = "Go Straight and take a right. You have reached your destination.";
                            break;
                        default: text = "Go Straight"; break;

                    }
                    navigationView.setVisibility(View.VISIBLE);
                    navigation.append(text + "\n");
                    pos++;
                }else if(pos == 1 && timeElapsed < threshold){
                    Toast.makeText(IndoorActivity.this, "Li-fi detected", Toast.LENGTH_SHORT).show();
                    String text;
                    switch (parkingSpot){
                        case "3": text = "Go Left. You have reached your destination.";
                            pos++;
                            break;
                        case "4": text = "Go Straight and take a left. You have reached your destination.";
                            pos++;
                            break;
                        case "7": text = "Go Right. You have reached your destination.";
                            pos++;
                            break;
                        case "8": text = "Go Straight and take a right. You have reached your destination.";
                            pos++;
                            break;
                        default: text = ""; break;

                    }
                    navigation.append(text);

                }
//                Log.d("Time elapsed", String.valueOf(timeElapsed));
//                Toast.makeText(MainActivity.this, "TIME ON = " + timeElapsed, Toast.LENGTH_LONG).show();
                timeStart = -1;
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
}
