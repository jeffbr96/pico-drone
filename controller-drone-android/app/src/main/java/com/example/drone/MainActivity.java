package com.example.drone;

import android.graphics.Color;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.ToggleButton;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.textfield.TextInputEditText;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {
    public ToggleButton connectionStatus;
    public TextView messagelog;
    public TextInputEditText messageBox;
    public static String message = "";

    // file for .csv file to be written to android/data/...
    public static String fileName = "";
    // server info
    ServerSocket serverSocket;
    public static String SERVER_IP = "";
    public final int SERVER_PORT = 10000;

    @Override
    protected void onCreate(Bundle saveInstanceState) {
        super.onCreate(saveInstanceState);

        // Prevent device from sleeping
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.layout);
        connectionStatus = findViewById(R.id.tvIP);
        messagelog = findViewById(R.id.message1);
        messageBox = findViewById(R.id.inputText1);

        try {
            SERVER_IP = getIp();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        new Thread(new Thread1()).start();
    }

    public void buttonClick(View view){
        int viewID = view.getId();
        //please change me to something more meaningfull
        if(viewID == R.id.calibrate){
            messageBox.setText("calibrate");
            viewID = R.id.send;
        }

        if(viewID == R.id.run){
            messageBox.setText("run");
            viewID = R.id.send;
        }
        if(viewID == R.id.stop){
            messageBox.setText("stop");
            viewID = R.id.send;
        }

        if(viewID == R.id.send){
            message = Objects.requireNonNull(messageBox.getText()).toString().trim();
            new Thread(new Thread3(message)).start();
            System.out.println("Message sent");
        }

    }

    private String getIp() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int INT_IP = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(INT_IP).array()).getHostAddress();
    }

    // Thread 1 code
    private PrintWriter output;
    private BufferedReader input;

    class Thread1 implements Runnable{
        @Override
        public void run(){
            Socket socket;
            try{
                ServerSocket serverSocket = new ServerSocket(SERVER_PORT);
                runOnUiThread(() -> connectionStatus.setText(SERVER_IP));
                try{
                    socket = serverSocket.accept();
                    output = new PrintWriter(socket.getOutputStream());
                    input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    connectionStatus.setChecked(true);
                    connectionStatus.setTextColor(Color.GREEN);
                    new Thread(new Thread2()).start();
                }catch(IOException e){
                    e.printStackTrace();
                }
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    class Thread2  implements Runnable{
        @Override
        public void run(){
            while(true){
                try{
                    final String message = input.readLine();
                    if(message != null){
                        runOnUiThread(() -> messagelog.append(message));
                    }else{
                        new Thread(new Thread1()).start();
                    }
                }catch(IOException e){
                    e.printStackTrace();
                }
            }
        }
    }

    private class Thread3 implements Runnable {
        private final String message;
        Thread3(String message){
            this.message = message;
        }
        @Override
        public void run(){
            output.write(message);
            output.flush();
            runOnUiThread(() -> {
                messagelog.append("Server:\t" + message + "\n");
            });
        }
    }

}
