package me.org.sampletest;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;


public class MainActivity extends AppCompatActivity {

    EditText editText;
    TextView textView;
    Bundle savedInstanceState;
    IntentIntegrator intentIntegrator;
    Button button;
    String mess;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.savedInstanceState = savedInstanceState;
        setContentView(R.layout.activity_main);
//        editText = (EditText) findViewById(R.id.editText);
//        textView = (TextView) findViewById(R.id.textView3);
        button = (Button) findViewById(R.id.button_2);
        intentIntegrator = new IntentIntegrator(this);
        sampleScan(button);
    }


//    public void sample_click (View view)
//    {
//        String text = editText.getText().toString();
//
//        if(!text.equals(""))
//        {
//            try {
//                               QRCodeWriter qrCodeWriter = new QRCodeWriter();
//                ByteMatrix bitMatrix = qrCodeWriter.encode(text,BarcodeFormat.QR_CODE, 200,200);
//                int width = bitMatrix.getWidth();
//                Bitmap bmp = Bitmap.createBitmap(width, width, Bitmap.Config.RGB_565);
//                for (int x = 0; x < width; x++) {
//                    for (int y = 0; y < width; y++) {
//                        bmp.setPixel(y, x, bitMatrix.get(x, y)==0 ? Color.BLACK : Color.WHITE);
//                    }
//                }
//
//                Intent intent = new Intent(this,Main2Activity.class);
//                intent.putExtra("image",bmp);
//                startActivity(intent);
//
//            } catch (Exception e) {
//                e.printStackTrace();
//            }
//        }
//    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult intentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);

        if (intentResult != null) {
            if (intentResult.getContents() == null) {
//                Toast.makeText(this, "Unable to scan", Toast.LENGTH_LONG).show();
            } else {
                String obj = new String(intentResult.getContents());
                Toast.makeText(this, obj, Toast.LENGTH_LONG).show();
                mess = obj;
                makeRequest(mess);
            }
        }

//        onCreate(savedInstanceState);
    }

    @Override
    protected void onResume() {
        super.onResume();
        sampleScan(button);
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

//    @Override
//    protected void onStop() {
//        finish();
//        super.onStop();
//        onStart();
//    }

    //    public void sample_get (View view)
//    {
//        Intent intent = new Intent(this,Main3Activity.class);
//        intent.putExtra("message",mess);
//        startActivity(intent);
//    }

    public void makeRequest(String message){
        SendMessage msg = new SendMessage();
        msg.execute(message);
    }

    public void sampleScan(View view) {
        intentIntegrator.initiateScan();
    }
}
