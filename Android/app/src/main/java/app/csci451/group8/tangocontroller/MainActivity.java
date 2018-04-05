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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button talkActivityButton = findViewById(R.id.enterTtsView);
        Button changeTextButton = findViewById(R.id.changeText);
        talkActivityButton.setOnClickListener(this);
        changeTextButton.setOnClickListener(this);

        Intent speech = new Intent(this, PocketSphinxActivity.class);
        startActivity(speech);

//        sr = SpeechRecognizer.createSpeechRecognizer(this);
//        sr.setRecognitionListener(new SpeechListener());
//        sr.startListening(new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH));
    }

    public void onClick(View view) {

    }

    private void enterTTS() {
        Intent tts = new Intent(this, TTSWindow.class);
        startActivity(tts);
    }

    private void changeLabelText() {
        EditText text = findViewById(R.id.textChange);
        text.setText("Changed", TextView.BufferType.EDITABLE);
    }
}
