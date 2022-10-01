package com.example.drone;

import android.graphics.Color;
import android.widget.ToggleButton;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Threads {

    public final int SERVER_PORT = 10000;
    public ToggleButton connectionStatus;
    public static String SERVER_IP = "";

    private PrintWriter output;
    private BufferedReader input;

    class Thread1 implements Runnable{
        @Override
        public void run(){
            Socket socket;
            try{
                ServerSocket serverSocket = new ServerSocket(SERVER_PORT);
                connectionStatus.setText(SERVER_IP);
                try{
                    socket = serverSocket.accept();
                    output = new PrintWriter(socket.getOutputStream());
                    input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                    connectionStatus.setChecked(true);
                    connectionStatus.setTextColor(Color.GREEN);
                    //new Thread(new Thread2()).start();
                }catch(IOException e){
                    e.printStackTrace();
                }
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }
}
