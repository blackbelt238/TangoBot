package app.csci451.group8.tangocontroller;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button talkActivityButton = findViewById(R.id.enterTtsView);
        Button changeTextButton = findViewById(R.id.changeText);
        talkActivityButton.setOnClickListener(this);
        changeTextButton.setOnClickListener(this);
    }

    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.enterTtsView:
                enterTTS();
                break;
            case R.id.changeText:
                changeLabelText();
                break;
        }
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
