package app.csci451.group8.tangocontroller;

import android.content.Intent;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;


// STT HELP FROM https://www.vladmarton.com/pocketsphinx-continuous-speech-recognition-android-tutorial/
// USING POCKETSPHINX LIBRARY FOR STT

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    TextView responses;
    EditText ipInput;
    Button ipButton;
    Server server;
    TTS tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipButton = findViewById(R.id.ipButton);
        ipButton.setOnClickListener(this);

        TextView ipNum = findViewById(R.id.ipNum);
        server = new Server(this);
        ipNum.setText(server.getIpAddress());

        ipInput = findViewById(R.id.ipInput);

    }

    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.ipButton:
                if (checkConnection()) {
                    tts = new TTS(this);
                    tts.start();

                    Intent speech = new Intent(this, PocketSphinxActivity.class);
                    startActivity(speech);
                }
                break;
        }
    }

    private boolean checkConnection() {
        String ip = ipInput.getText().toString();
        if (ip.isEmpty()) {
            return false;
        }
        Client checkResponse = new Client(ip, 5011, "Test");
        checkResponse.execute();

        if (checkResponse.responseAddr != null) {
            return true;
        }
        return false;
    }

}
