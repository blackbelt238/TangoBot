package com.example.una.network;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Server server;
    Client client;
    public TextView infoip, msg, response;
    public Button buttonConnect;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        response = findViewById(R.id.recieved_text);
        msg = findViewById(R.id.sendText);
        infoip = findViewById(R.id.ipArea);

        server = new Server(this);
        infoip.setText(server.getIpAddress() + ":" + server.getPort());

        buttonConnect = findViewById(R.id.sendButton);
        buttonConnect.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.sendButton:
                Client client = new Client("10.200.42.197", 5011, response);
                client.execute();
                break;
        }
    }
}
