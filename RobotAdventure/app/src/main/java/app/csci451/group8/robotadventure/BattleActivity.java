package app.csci451.group8.robotadventure;

import android.media.Image;
import android.media.MediaPlayer;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import app.csci451.group8.robotadventure.utils.NumUtils;
import app.csci451.group8.robotadventure.utils.ResponseParser;

public class BattleActivity extends AppCompatActivity implements View.OnClickListener{

    // Current stat bookkeeping
    private String enemyName;
    private int enemyHP;
    private int enemyMaxHP;
    private int ourHP;
    private int ourMaxHP;

    // HP stuff
    ProgressBar enemyHPBar;
    ProgressBar ourHPBar;

    TextView enemyNameText;

    Button attackButton;
    Button runButton;

    MediaPlayer mp;
    ImageButton enemyPortrait;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_battle);

        //Create on-screen views
        enemyHPBar = findViewById(R.id.enemyHealthBar);
        ourHPBar = findViewById(R.id.ourHealthBar);
        enemyNameText = findViewById(R.id.enemyName);
        attackButton = findViewById(R.id.attack_button);
        runButton = findViewById(R.id.run_button);

        // Set listeners
        attackButton.setOnClickListener(this);
        runButton.setOnClickListener(this);

        // Grab extras
        Bundle extras = getIntent().getExtras();
        this.enemyName = extras.getString("ENEMY_NAME");
        this.enemyHP = extras.getInt("STARTING_HP");
        this.enemyMaxHP = this.enemyHP;
        this.ourHP = extras.getInt("OUR_HP");
        this.ourMaxHP = extras.getInt("OUR_MAX_HP");

        // Fill view properties
        enemyHPBar.setMax(this.enemyHP);
        enemyNameText.setText(this.enemyName);
        ourHPBar.setMax(this.ourMaxHP);
        ourHPBar.setProgress(NumUtils.percentOf(this.ourHP, this.ourMaxHP));

        enemyPortrait = findViewById(R.id.imageButton);

        if (enemyName.equals("tiger")) {
            enemyPortrait.setImageResource(R.drawable.tiger);
        } else {
            enemyPortrait.setImageResource(R.drawable.snake);
        }

        //mp = MediaPlayer.create(getApplicationContext(), R)

    }

    @Override
    public void onDestroy() {

        super.onDestroy();
    }


    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.attack_button:
                attackEnemy();
                break;
            case R.id.run_button:
                runAway();
                break;
        }
    }

    private void attackEnemy() {
        attackButton.setEnabled(false);
        Client client = new Client(getString(R.string.pi_ip), Integer.parseInt(getString(R.string.pi_port)), "attack");
        while (client.responseAddr == null);
        if (client.responseAddr.equals("finish")) {
            finish();
        }
        List<String> hpVals = ResponseParser.parseAttackResponse(client.responseAddr);
        ourHP = Integer.parseInt(hpVals.get(0));
        enemyHP = Integer.parseInt(hpVals.get(1));

        ourHPBar.setProgress(NumUtils.percentOf(ourHP, ourMaxHP));
        enemyHPBar.setProgress(NumUtils.percentOf(enemyHP, enemyMaxHP));
        attackButton.setEnabled(true);
    }

    private void runAway() {
        runButton.setEnabled(false);
        Client client = new Client(getString(R.string.pi_ip), Integer.parseInt(getString(R.string.pi_port)), "run");
        while (client.responseAddr == null);
        finish();
    }
}
