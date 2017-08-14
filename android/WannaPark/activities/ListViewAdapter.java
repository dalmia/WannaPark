package me.org.wannapark;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by ADITYA on 6/22/2017.
 */
public class ListViewAdapter extends ArrayAdapter<Item> {
    int groupId;
    ArrayList<Item> itemList;
    Context context;

    public ListViewAdapter(Context context, int vg, ArrayList<Item> itemList) {
        super(context, vg, itemList);
        this.context = context;
        groupId = vg;
        this.itemList = itemList;

    }

    // Hold views of the ListView to improve its scrolling performance
    static class ViewHolder {
        public TextView spotName;
        public TextView address;
        public TextView city;
        public ImageView imageView;
        public ImageView status;
        public TextView estTime;
    }

    public View getView(int position, View convertView, ViewGroup parent) {

        View rowView = convertView;
        // Inflate the list_item.xml file if convertView is null
        if (rowView == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            rowView = inflater.inflate(groupId, parent, false);
            ViewHolder viewHolder = new ViewHolder();
            viewHolder.spotName = (TextView) rowView.findViewById(R.id.spotName);
            viewHolder.address = (TextView) rowView.findViewById(R.id.address);
            viewHolder.city = (TextView) rowView.findViewById(R.id.city);
            viewHolder.imageView = (ImageView) rowView.findViewById(R.id.imageView4);
            viewHolder.status = (ImageView) rowView.findViewById(R.id.status);
            viewHolder.estTime = (TextView) rowView.findViewById(R.id.eta);
            rowView.setTag(viewHolder);

        }
        // Set text to each TextView of ListView item
        ViewHolder holder = (ViewHolder) rowView.getTag();
        if(itemList.get(position).estTime.equals("00:00:00")){
            holder.status.setImageResource(R.drawable.ic_status_green);
            holder.estTime.setText("Currently Available");
        }else{
            holder.status.setImageResource(R.drawable.ic_status_red);
            Log.d("Yo", itemList.get(position).estTime);
            Log.d("Yo", itemList.get(position).spotName);
            String hour = itemList.get(position).estTime.split(":")[0];
            String minute = itemList.get(position).estTime.split(":")[1];
            holder.estTime.setText("Available at "  + hour + ":" + minute);
        }

        switch (itemList.get(position).spotName) {
            case "lot_a":
                holder.spotName.setText("Qualcomm C Building");
                holder.address.setText("Plot 153-154, EPIP Zone");
                holder.city.setText("Whitefield, Bangalore");
                holder.imageView.setImageResource(R.drawable.icon1);
                break;

            case "lot_b":
                holder.spotName.setText("Qualcomm E Building");
                holder.address.setText("186,Phase II, EPIP Zone");
                holder.city.setText("Whitefield, Bangalore");
                holder.imageView.setImageResource(R.drawable.icon2);
                break;

            case "lot_c":
                holder.spotName.setText("Qualcomm B Building");
                holder.address.setText("176, Adarsh Eco Place,EPIP Zone");
                holder.city.setText("Whitefield, Bangalore");
                holder.imageView.setImageResource(R.drawable.icon3);
                break;
        }
        return rowView;
    }

}
