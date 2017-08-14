package me.org.wannapark;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import org.json.JSONException;

import java.util.Calendar;

import me.org.wannapark.app.Config;
import me.org.wannapark.utils.Response;
import me.org.wannapark.utils.Spot;
import me.org.wannapark.utils.Utils;

import static me.org.wannapark.app.Config.KEY_ETA;
import static me.org.wannapark.app.Config.KEY_VALUE;
import static me.org.wannapark.app.Config.SUCCESS;

public class LocationSelectActivity extends Activity implements Response{

    ImageView imageViewMap;
    TextView textViewName;
    TextView textViewAddress;
    TextView textViewCity;
    String value;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_location_select);
        imageViewMap = (ImageView) findViewById(R.id.parkMap);
        textViewName = (TextView) findViewById(R.id.name);
        textViewAddress = (TextView) findViewById(R.id.address);
        textViewCity = (TextView) findViewById(R.id.city);
        Intent intent = getIntent();
        value = intent.getStringExtra(KEY_VALUE);
        Spot spot = Spot.valueOf(value);
        switch (spot) {
            case lot_a:
                textViewName.setText("Qualcomm C Building");
                textViewAddress.setText("Plot 153-154,EPIP Zone");
                textViewCity.setText("Whitefield, Bangalore");
                imageViewMap.setImageResource(R.drawable.map1);
                break;

            case lot_b:
                textViewName.setText("Qualcomm E Building");
                textViewAddress.setText("186,Phase II,EPIP Zone");
                textViewCity.setText("Whitefield, Bangalore");
                imageViewMap.setImageResource(R.drawable.map2);
                break;

            case lot_c:
                textViewName.setText("Qualcomm B Building");
                textViewAddress.setText("176,Adarsh Eco Place,EPIP Zone");
                textViewCity.setText("Whitefield, Bangalore");
                imageViewMap.setImageResource(R.drawable.map3);
                break;
        }
    }

    public void onClickButton(View view) throws JSONException {
        Utils.makeRequest("BOOK::"  + value, String.valueOf(Config.PORT1), this,true);
//        Intent intent = new Intent(LocationSelectActivity.this, QRActivity.class);
//        intent.putExtra(KEY_VALUE, value);
//        startActivity(intent);
    }

    @Override
    public void processFinish(String output) {
        final Intent intent;
        if(output.equals(SUCCESS)){
            intent = new Intent(LocationSelectActivity.this, QRActivity.class);
            AlertDialog.Builder builder =
                    new AlertDialog.Builder(this, R.style.AppCompatAlertDialogStyle);
            LayoutInflater inflater=this.getLayoutInflater();
            View dialog = inflater.inflate(R.layout.dialog, null);
            builder.setView(dialog);
            final EditText usernameInput=(EditText)dialog.findViewById(R.id.eta_entered);
            usernameInput.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Calendar mCurrentTime = Calendar.getInstance();
                    int hour = mCurrentTime.get(Calendar.HOUR_OF_DAY);
                    int minute = mCurrentTime.get(Calendar.MINUTE);
                    TimePickerDialog mTimePicker;
                    mTimePicker = new TimePickerDialog(LocationSelectActivity.this, new TimePickerDialog.OnTimeSetListener() {
                        @Override
                        public void onTimeSet(TimePicker timePicker, int selectedHour, int selectedMinute) {
                            usernameInput.setText( selectedHour + ":" + selectedMinute);
                        }
                    }, hour, minute, true);//Yes 24 hour time
                    mTimePicker.setTitle("Select Time");
                    mTimePicker.show();
                }
            });

            builder.setTitle("Dialog");
            builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {
                    if(usernameInput.getText().toString().length() == 0){
                        Toast.makeText(LocationSelectActivity.this, "Enter expected time of Departure", Toast.LENGTH_SHORT);
                    }else{
                        intent.putExtra(KEY_VALUE, value);
                        String estTime = usernameInput.getText().toString();
                        int hour = Integer.valueOf(estTime.split(":")[0]);
                        int minute = Integer.valueOf(estTime.split(":")[1]);
                        int hourDifference = hour - Calendar.getInstance().get(Calendar.HOUR_OF_DAY);
                        int minDifference = (minute - Calendar.getInstance().get(Calendar.MINUTE)+ 60) % 60;
                        int seconds = hourDifference * 3600 + minDifference * 60;
                        intent.putExtra(KEY_ETA, seconds);
                        startActivity(intent);

                    }
                }
            });
            builder.setNegativeButton("Cancel", null);
            builder.show();
        }else{
            Toast.makeText(LocationSelectActivity.this, "Sorry, the  parking spot is gone!!",  Toast.LENGTH_LONG);
            intent = new Intent(LocationSelectActivity.this, ListAvailable.class);
            startActivity(intent);
        }

    }
}
