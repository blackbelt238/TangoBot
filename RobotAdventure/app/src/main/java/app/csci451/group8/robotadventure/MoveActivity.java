package app.csci451.group8.robotadventure;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import java.util.ArrayList;
import java.util.HashMap;

public class MoveActivity extends AppCompatActivity implements View.OnClickListener{

    Button north, south, east, west, chest, station;
    HashMap<String, Button> buttons;
    ArrayList<String> actions;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_move);

        actions = getIntent().getExtras().getStringArrayList("POSSIBLE_ACTIONS");

        buttons.put("north", north = findViewById(R.id.northButton));
        buttons.put("south", south = findViewById(R.id.southButton));
        buttons.put("east", east = findViewById(R.id.eastbutton));
        buttons.put("west", west = findViewById(R.id.westButton));
        buttons.put("chest", chest = findViewById(R.id.chestButton));
        buttons.put("station", station = findViewById(R.id.chargeButton));

        north.setOnClickListener(this);
        south.setOnClickListener(this);
        east.setOnClickListener(this);
        west.setOnClickListener(this);
        chest.setOnClickListener(this);
        station.setOnClickListener(this);

        disableAll();
        enablePossibleActions(actions);
    }

    @Override
    public void onClick(View view) {
        disableAll();
        String button = ((Button) findViewById(view.getId())).getText().toString();
        Client client = new Client(getString(R.string.pi_ip), Integer.parseInt(getString(R.string.pi_port)), button);
        while(client.responseAddr == null);
        if (client.responseAddr.equals("need key")) {
            actions.remove("station");
            enablePossibleActions(actions);
            return;
        }
        finish();
    }

    private void enablePossibleActions(ArrayList<String> actions) {
        for (String action : actions) {
            if (buttons.containsKey(action.toLowerCase())) {
                buttons.get(action.toLowerCase()).setEnabled(true);
            }
        }
    }

    private void disableAll() {
        north.setEnabled(false);
        south.setEnabled(false);
        east.setEnabled(false);
        west.setEnabled(false);
        chest.setEnabled(false);
        station.setEnabled(false);
    }
}
