import 'package:flutter/material.dart';
import 'package:localup/login_screen.dart';
import 'package:localup/audio_player.dart';

void main() => runApp(new MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Flutter Login Screen 1',
      theme: new ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: new AudioApp(),
      debugShowCheckedModeBanner: false,
    );
  }
}



