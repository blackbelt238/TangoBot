package app.csci451.group8.robotadventure;

import android.app.Activity;
import android.app.Notification;
import android.os.Bundle;
import android.os.Message;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.lang.reflect.Array;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;

public class GameServer {
    Activity activity;
    ServerSocket serverSocket;
    String receivedMessage;
    static final int socketServerPORT = 5011;

    public GameServer(Activity activity) {
        this.activity = activity;
        Thread socketServerThread = new Thread(new SocketServerThread());
        socketServerThread.start();
    }

    public int getPort() {
        return socketServerPORT;
    }

    public void onDestroy() {
        if (serverSocket != null) {
            try {
                System.out.println("Destroying");
                serverSocket.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }


    private class SocketServerThread extends Thread {

        int count = 0;

        private String processMessage(String message) {
            if (message.equals("What class?")) {
                return "wizard";
            }

            if (message.contains("travel")) {
                message = message.replace("travel:", "");
                ArrayList<String> actions = new ArrayList<String>(Arrays.asList(message.split(",")));
                ((MainActivity) activity).actions = actions;
                ((MainActivity) activity).enablePossibleActions(actions);
            }
            return null;
        }

        @Override
        public void run() {
            try {
                // create ServerSocket using specified port
                serverSocket = new ServerSocket(socketServerPORT);

                while (true) {
                    // block the call until connection is created and return
                    // Socket object
                    Socket socket = serverSocket.accept();
                    System.out.println(socket.getInetAddress() + ":" + socket.getPort());
                    count++;
                    BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    receivedMessage = input.readLine();
                    String response = processMessage(receivedMessage);

                    SocketServerReplyThread socketServerReplyThread =
                            new SocketServerReplyThread(socket, response,  count);
                    socketServerReplyThread.run();

                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    private class SocketServerReplyThread extends Thread {

        private Socket hostThreadSocket;
        private String message;
        int cnt;

        SocketServerReplyThread(Socket socket, String message, int c) {
            hostThreadSocket = socket;
            this.message = message;
            cnt = c;
        }

        @Override
        public void run() {
            OutputStream outputStream;

            try {
                outputStream = hostThreadSocket.getOutputStream();
                PrintStream printStream = new PrintStream(outputStream);
                printStream.println(message);
                printStream.close();

                //message += "replayed: " + msgReply + "\n";


            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
                receivedMessage += "Something wrong! " + e.toString() + "\n";
            }
        }

    }

    public static String getIpAddress() {
        String ipAddress = "Unable to Fetch IP..";
        try {
            Enumeration en;
            en = NetworkInterface.getNetworkInterfaces();
            while ( en.hasMoreElements()) {
                NetworkInterface intf = (NetworkInterface)en.nextElement();
                for (Enumeration enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = (InetAddress)enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()&&inetAddress instanceof Inet4Address) {
                        ipAddress=inetAddress.getHostAddress().toString();
                        return ipAddress;
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return ipAddress;
    }
}
