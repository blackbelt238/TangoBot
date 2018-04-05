package app.csci451.group8.tangocontroller;

import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class TTSWindow extends AppCompatActivity implements View.OnClickListener{

    TTS tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ttswindow);

        Button ttsButton = findViewById(R.id.ttsButton);
        ttsButton.setOnClickListener(this);

        tts = new TTS(this);
        tts.start();
    }


    protected void onDestroy() {
        tts.destroy();
        super.onDestroy();
        //unbindService(tts);
    }


    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.ttsButton:
                Message sendMsg = tts.handler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("TT", getString(R.string.disgust));
                sendMsg.setData(b);
                tts.handler.sendMessage(sendMsg);
                break;
        }
    }
}
