package me.org.wannapark;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.common.ByteMatrix;
import com.google.zxing.qrcode.QRCodeWriter;

import me.org.wannapark.app.Config;

import static me.org.wannapark.app.Config.KEY_COST;
import static me.org.wannapark.app.Config.KEY_HOURS;
import static me.org.wannapark.app.Config.KEY_MINUTES;
import static me.org.wannapark.app.Config.KEY_SECONDS;

public class ExitActivity extends Activity {

    TextView textViewTime;
    TextView textViewFare;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_exit);
        textViewTime = (TextView) findViewById(R.id.exitTime);
        textViewFare = (TextView) findViewById(R.id.fare);

        Intent intent = getIntent();

        int diffHr = intent.getIntExtra(KEY_HOURS,0);
        int diffMin = intent.getIntExtra(KEY_MINUTES,0);
        int diffSec = intent.getIntExtra(KEY_SECONDS,0);
        int cost = intent.getIntExtra(KEY_COST,0);

        textViewTime.setText("Total Time Elapsed : "+diffHr+":"+diffMin+":"+diffSec);
        textViewFare.setText("Total Fare : INR "+cost+" only");
    }

    @Override
    public void onBackPressed() {
        Intent intent = new Intent(getApplicationContext(), ListAvailable.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        intent.putExtra("EXIT", true);
        startActivity(intent);

    }

    public void onClick(View view){
        onBackPressed();
    }
}
