package me.org.wannapark;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;

import me.org.wannapark.app.Config;
import me.org.wannapark.utils.Response;
import me.org.wannapark.utils.SendMessage;
import me.org.wannapark.utils.Utils;

import static me.org.wannapark.app.Config.KEY_EXIT;
import static me.org.wannapark.app.Config.KEY_VALUE;
import static me.org.wannapark.app.Config.PORT1;

public class ListAvailable extends Activity implements Response {

    Context context;
    Item[] items;
    ImageButton button;
    String msg = "LOT_QUERY";
    ListView listView;
    ListViewAdapter listViewAdapter;

    ProgressDialog pDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list_available);
        if (getIntent().getBooleanExtra(KEY_EXIT, false)) {
            finish();
        }

        context = this;
        listView = (ListView) findViewById(R.id.listview);
        button = (ImageButton) findViewById(R.id.refreshButton);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                pDialog = new ProgressDialog(ListAvailable.this);
                pDialog.setMessage("Fetching available spots...");
                pDialog.setCancelable(true);
                pDialog.show();
                Utils.makeRequest(msg, String.valueOf(PORT1), ListAvailable.this, true);
            }
        });


        pDialog = new ProgressDialog(this);
        pDialog.setMessage("Fetching available spots...");
        pDialog.setCancelable(true);
        pDialog.show();
        Utils.makeRequest(msg, String.valueOf(PORT1), this, true);

//        final ArrayList<String> items = new ArrayList();
//        items.add("A");
//        items.add("B");
//        items.add("C");
//
//        listViewAdapter = new ListViewAdapter(this, R.layout.list_element, items);
//        listView.setAdapter(listViewAdapter);
//
//        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
//            @Override
//            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
//
//                Intent intent = new Intent(context, LocationSelectActivity.class);
//                intent.putExtra("value", items.get(i));
//                context.startActivity(intent);
//
//
//            }
//        });

    }

    @Override
    public void processFinish(String output) {
        if (output != null) {
            pDialog.cancel();
            ArrayList<String> res = new ArrayList(Arrays.asList(output.split("::")));
            res.remove(0);
            res.remove(0);

            final ArrayList<Item> items = new ArrayList();
            items.add(new Item(res.get(0), res.get(1)));
            items.add(new Item(res.get(2), res.get(3)));
            items.add(new Item(res.get(4), res.get(5)));

            listViewAdapter = new ListViewAdapter(this, R.layout.list_element, items);
            listView.setAdapter(listViewAdapter);

            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                    if(!items.get(i).estTime.equals("00:00:00")){
                        Toast.makeText(ListAvailable.this, "No parking spots currently available here", Toast.LENGTH_SHORT).show();
                    }
                    else {
                        Intent intent = new Intent(context, LocationSelectActivity.class);
                        intent.putExtra(KEY_VALUE, items.get(i).spotName);
                        context.startActivity(intent);
                    }
                }
            });
        }
    }
}
