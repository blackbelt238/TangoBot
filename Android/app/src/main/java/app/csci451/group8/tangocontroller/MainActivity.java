package app.csci451.group8.tangocontroller;

import android.content.Intent;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import edu.cmu.pocketsphinx.SpeechRecognizer;


// STT HELP FROM https://www.vladmarton.com/pocketsphinx-continuous-speech-recognition-android-tutorial/
// USING POCKETSPHINX LIBRARY FOR STT

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    TextView responses, clientText;
    Button clientButton;
    Server server;
    TTS tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        responses = findViewById(R.id.messageView);
        clientText = findViewById(R.id.clientText);

        clientButton = findViewById(R.id.clientButton);
        clientButton.setOnClickListener(this);

        TextView ipNum = findViewById(R.id.ipNum);
        tts = new TTS(this);
        tts.start();

        server = new Server(this);
        ipNum.setText(server.getIpAddress());
        Intent speech = new Intent(this, PocketSphinxActivity.class);
        startActivity(speech);

    }

    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.clientButton:
                Client client = new Client(getString(R.string.pi_ip), 5011, clientText.getText().toString());
                client.execute();
                break;
        }
    }

}
