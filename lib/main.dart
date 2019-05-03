import 'package:flutter/material.dart';
import 'package:localup/audio_player.dart';
import 'package:localup/start_pages.dart';

void main() {
  runApp(MaterialApp(
    home: StartPage(), // becomes the root named '/'
    routes: <String, WidgetBuilder> {
      // context from BuildContext
      '/Login': (context) => LoginPage(),
      '/Signup': (context) => SignupPage(),
      '/GenrePage': (context) => GenrePage(),

      '/AudioPlayer': (context) => AudioApp(),
    },
  ));
}

//class MyApp extends StatelessWidget {
//  @override
//  Widget build(BuildContext context) {
//    return new MaterialApp(
//      title: 'Flutter Login Screen 1',
//      theme: new ThemeData(
//        primarySwatch: Colors.blue,
//      ),
//      //home: new LoginScreen(),
//      home: new AudioApp(),
//      debugShowCheckedModeBanner: false,
//    );
//  }
//}


