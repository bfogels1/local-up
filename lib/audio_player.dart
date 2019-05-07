import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'dart:convert';

import 'package:audioplayer/audioplayer.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/services.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';

typedef void OnError(Exception exception);

var kUrl = 'https://s0.vocaroo.com/media/download_temp/Vocaroo_s02PXvSfMGrO.mp3';
var artist = 'THE DEEP END';
var song = 'Heavy Water';
var bio = 'Formed in 2017, THE DEEP END has gained attention for its resonant '
    'lyrics, diverse rhythms and soaring choruses. While the band\'s first single, heavy water, is '
    'noteworthy for its layered, lush production, THE DEEP END is built around crunching guitars  '
    'and a rock-solid rhythm section that drives its music unrelentingly forward. '
    'In an era where many have proclaimed rock music dead, THE DEEP END\'s music '
    'serves as a reminder of the genre\'s power and continued relevance. \n\n';

List<T> map<T>(List list, Function handler) {
  List<T> result = [];
  for (var i = 0; i < list.length; i++) {
    result.add(handler(i, list[i]));
  }

  return result;
}

/*
List<String> imgList = [
  'https://images.unsplash.com/photo-1522863602463-afebb8886ab2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
  'https://images.unsplash.com/photo-1522536421511-14c9073df899?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80',
  'https://images.unsplash.com/photo-1508695666381-69deeaa78ccb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
  'https://images.unsplash.com/photo-1550056462-07f9fa8fb9b8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1376&q=80',
  'https://images.unsplash.com/photo-1541428973141-3e739c202d9e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80'
];
*/

List<String> imgList = [
  'https://scontent-iad3-1.cdninstagram.com/vp/d1cf83d80cfe80fc60b842c6ed62d691/5D7026C4/t51.2885-15/e35/47694641_382201942585775_1964758380600414909_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com',
  'https://scontent-iad3-1.cdninstagram.com/vp/11b7e89844a01f22dfa41477a285b510/5D5236B9/t51.2885-15/e35/50574470_376739999550131_1391391369206455161_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com',
  'https://scontent-iad3-1.cdninstagram.com/vp/5ffb4bf568606076154848256f11c020/5D559ADF/t51.2885-15/e35/43054384_293767881243690_4971574116922731125_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com'
];


void main() {
  runApp(new MaterialApp(home: new Scaffold(body: new AudioApp())));
}

enum PlayerState { stopped, playing, paused }

class AudioApp extends StatefulWidget {
  @override
  _AudioAppState createState() => new _AudioAppState();
}

class _AudioAppState extends State<AudioApp> {

  Duration duration;
  Duration position;

  AudioPlayer audioPlayer;

  String localFilePath;

  PlayerState playerState = PlayerState.stopped;

  get isPlaying => playerState == PlayerState.playing;
  get isPaused => playerState == PlayerState.paused;

  get durationText =>
      duration != null ? duration.toString().split('.').first : '';
  get positionText =>
      position != null ? position.toString().split('.').first : '';

  bool isMuted = false;

  StreamSubscription _positionSubscription;
  StreamSubscription _audioPlayerStateSubscription;

  @override
  void initState() {
    super.initState();
    initAudioPlayer();
  }

  @override
  void dispose() {
    _positionSubscription.cancel();
    _audioPlayerStateSubscription.cancel();
    audioPlayer.stop();
    super.dispose();
  }

  void initAudioPlayer() {
    audioPlayer = new AudioPlayer();
    _positionSubscription = audioPlayer.onAudioPositionChanged
        .listen((p) => setState(() => position = p));
    _audioPlayerStateSubscription =
        audioPlayer.onPlayerStateChanged.listen((s) {
          if (s == AudioPlayerState.PLAYING) {
            setState(() => duration = audioPlayer.duration);
          } else if (s == AudioPlayerState.STOPPED) {
            onComplete();
            setState(() {
              position = duration;
            });
          }
        }, onError: (msg) {
          setState(() {
            playerState = PlayerState.stopped;
            duration = new Duration(seconds: 0);
            position = new Duration(seconds: 0);
          });
        });
  }

  IconData ppIcon = Icons.pause;

  Future play() async {
    await audioPlayer.play(kUrl);
    setState(() {
      playerState = PlayerState.playing;
    });
  }

  Future nextSong() async {
    //var url = 'http://127.0.0.1:5000/users/next_song';
    print('Url: $kUrl');

    var url = 'https://local-up-heroku.herokuapp.com/users/next_song';
    var response = await post(
        url,
        headers: {
        "Content-Type": "application/json",
        'Accept': 'application/json'},
        body: json.encode({'radio_name': 'LocalUp Radio'}));
    //print('Response status: ${response.statusCode}');
    //print('Response body: ${response.body}');
    var jsonResponse = jsonDecode(response.body);
    kUrl = jsonResponse['url'];
    print('Url: $kUrl');
    stop();
    play();
    updateInfo();
  }

  Future updateInfo() async {
    var url = 'https://local-up-heroku.herokuapp.com/radio/get_info';
    var response = await post(
        url,
        headers: {
          "Content-Type": "application/json",
          'Accept': 'application/json'},
        body: json.encode({'url': kUrl}));
    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');
    var jsonResponse = jsonDecode(response.body);
    var pics = jsonResponse['pics'];
    //imgList = pics.Cast<String>().ToList();
    imgList = pics.cast<String>();
    //imgList = pics;
    artist = jsonResponse['artist'];
    song = jsonResponse['song'];
    bio = jsonResponse['bio'];

  }

  Future _playLocal() async {
    await audioPlayer.play(localFilePath, isLocal: true);
    setState(() => playerState = PlayerState.playing);
  }

  Future pause() async {
    await audioPlayer.pause();
    setState(() {
      playerState = PlayerState.paused;
    });
  }

  Future stop() async {
    await audioPlayer.stop();
    setState(() {
      playerState = PlayerState.stopped;
      position = new Duration();
    });
  }

  Future mute(bool muted) async {
    await audioPlayer.mute(muted);
    setState(() {
      isMuted = muted;
    });
  }

  void onComplete() {
    setState(() => playerState = PlayerState.stopped);
    //nextSong();
  }

  Future<Uint8List> _loadFileBytes(String url, {OnError onError}) async {
    Uint8List bytes;
    try {
      bytes = await readBytes(url);
    } on ClientException {
      rethrow;
    }
    return bytes;
  }

  Future _loadFile() async {
    final bytes = await _loadFileBytes(kUrl,
        onError: (Exception exception) =>
            print('_loadFile => exception $exception'));

    final dir = await getApplicationDocumentsDirectory();
    final file = new File('${dir.path}/audio.mp3');

    await file.writeAsBytes(bytes);
    if (await file.exists())
      setState(() {
        localFilePath = file.path;
      });
  }

//  _onSelectItem(int index) {
//    setState(() => _selectedDrawerIndex = index);
//    Navigator.of(context).pop(); // close the drawer
//  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        backgroundColor: Colors.redAccent,
        // LOGO
        title: Image.asset('assets/images/localup_white_small.png'),

        leading: IconButton(
          icon: Icon(Icons.menu),
          iconSize: 30.0,
          onPressed: () {},
          // onPressed:() => Navigator.of(context).pop(),
          // onTap: () {}
        ),
      ),

        // HAMBURGER MENU
      drawer: new Drawer(
        child: ListView(
          // Important: Remove any padding from the ListView.
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              child: Text('Drawer Header'),
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
            ),
            ListTile(
              title: Text('Edit Genre Preferences'),
              onTap: () {
                // Update the state of the app
                Navigator.of(context).pop();
                Navigator.pushNamed(context, '/GenrePage');
              },
            ),
            ListTile(
              title: Text('Edit Location Preferences'),
              onTap: () {
                // Update the state of the app
                Navigator.of(context).pop();
                Navigator.pushNamed(context, '/LocationPage');
              },
            ),
          ],
        )
      ),

      body: new Column(
        children: [
          /*** SCROLLABLE LIST ***/
          new ConstrainedBox (
            //constraints: BoxConstraints.expand(height: MediaQuery.of(context).size.height*0.7),
              constraints: BoxConstraints.expand(height: MediaQuery.of(context).size.height*0.66),
          child: new ListView (
            shrinkWrap: true,
            children: <Widget>[
              /*** CAROUSEL ***/
              new Container(
                padding: EdgeInsets.symmetric(vertical: 16.0),
                child: CarouselSlider(
                  height: 300.0,
                  enlargeCenterPage: true,
                  enableInfiniteScroll: true,
                  items: map<Widget>(
                    imgList, //populated with deepend
                        (index, i) {
                      return Container(
                        margin: EdgeInsets.all(5.0),
                        child: new Material(
                          elevation: 2.0,
                          color: Colors.grey[200],
                          child: new Container (
                            decoration: BoxDecoration(
                            image: DecorationImage(image: NetworkImage(i), fit: BoxFit.cover),
                            )
                          ),
                        )
                      );
                    },
                  ),
                )
              ),
              /*** DIVIDER LINE ***/
              new Container (
                margin: new EdgeInsets.symmetric(horizontal: 30.0),
                child: new Divider(
                  color: Colors.black45,
                  height: 5.0,
                )
              ),
              new Container (
                child: new Row (
                  crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  new Container (
                      width: MediaQuery.of(context).size.width*0.7,
                      alignment: Alignment(-1.0, -1.0),
                      margin: new EdgeInsets.all(20.0),
                      //child: const Text.rich(
                      child: Text.rich(
                        TextSpan(
                          children: <TextSpan>[
                            //TextSpan(text: 'THE DEEP END\n\n', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 36.0)),
                            TextSpan(text: artist + '\n\n', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 36.0)),
                            /*TextSpan(text: 'Formed in 2017, THE DEEP END has gained attention for its resonant '
                                'lyrics, diverse rhythms and soaring choruses. While the band\'s first single, heavy water, is '
                                'noteworthy for its layered, lush production, THE DEEP END is built around crunching guitars  '
                                'and a rock-solid rhythm section that drives its music unrelentingly forward. '
                                'In an era where many have proclaimed rock music dead, THE DEEP END\'s music '
                                'serves as a reminder of the genre\'s power and continued relevance. \n\n'
                                , style: TextStyle(fontSize: 14.0)),*/
                            TextSpan(text: bio + '\n\n'
                                , style: TextStyle(fontSize: 14.0)),
                            TextSpan(text: 'Our mission:\n\n'
                                , style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20.0, color: Colors.black87)),
                            TextSpan(text: 'To provide the audience with a cathartic, high-quality live show, and keep them guessing. \n\n'
                                , style: TextStyle(fontSize: 14.0)),
                            TextSpan(text: 'What inspires you?\n\n'
                                , style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20.0, color: Colors.black87)),
                            TextSpan(text: 'Food, food is our true inspiration. We do not know where we would be without it.'
                                , style: TextStyle(fontSize: 14.0)),
                          ],
                        ),
                      )
                      ),
                      /*** SOCIAL ICONS ***/
                      new Container(
                        margin: new EdgeInsets.only(top: 70.0),
                        alignment: Alignment.topCenter,
                        child: Column(
                          children: [
                            new IconButton(
                                icon: new Icon(FontAwesomeIcons.instagram),
                                iconSize: 30.0,
                                color: Colors.black54),
                            new IconButton(
                                icon: new Icon(FontAwesomeIcons.facebook),
                                iconSize: 30.0,
                                color: Colors.black54),
                            new IconButton(
                                icon: new Icon(FontAwesomeIcons.twitter),
                                iconSize: 30.0,
                                color: Colors.black54),
                            new IconButton(
                                icon: new Icon(FontAwesomeIcons.spotify),
                                iconSize: 30.0,
                                color: Colors.black54),
                          ]
                        )
                      )
                    ]
                )
              )
            ]
          )
          ),
          /*** MUSIC PLAYER ***/
          new Container(
            alignment: Alignment.bottomCenter,
            child: new Column(
              mainAxisAlignment: MainAxisAlignment.end,
              mainAxisSize: MainAxisSize.max,
              children: [
                new Material(
                  child:
                  new Column(
                    children: [
                      _buildPlayer(),

                        localFilePath != null
                        ? new Text(localFilePath)
                        : new Container(),
                    ]
                  ),
                ),
              ]
            ),
          )
        ]
    )
  );
  }


  Widget _buildPlayer() => new Container(
      padding: new EdgeInsets.all(10.0),
      child: new Column(children: [
        new Text(
            'Baltimore Alternative Radio: ' + song,
            style: TextStyle(color: Colors.redAccent)
        ),
        new Row(mainAxisSize: MainAxisSize.max, children: [
          new Text(
              position != null
                  ? "${positionText ?? ''}"
                  : duration != null ? durationText : '',
              style: new TextStyle(color: Colors.redAccent, fontSize: 14.0),
          ),
          Expanded(

            child: duration == null || position == null
                ? new Slider(
                value: 0.0,
                min: 0.0,
                max: 1.0,
                activeColor: Colors.redAccent
                )
                :
                new Slider(
                value: position.inMilliseconds?.toDouble() ?? 0.0,
                onChanged: (double value) =>
                    audioPlayer.seek((value / 1000).roundToDouble()),
                min: 0.0,
                max: duration.inMilliseconds?.toDouble() ?? 1.0,
                activeColor: Colors.redAccent
            )
          ),
          new Text(
              position != null
                  ? "${durationText ?? ''}"
                  : duration != null ? durationText : '',
            style: new TextStyle(color: Colors.redAccent, fontSize: 14.0),
          )
        ]),
        new Row(mainAxisSize: MainAxisSize.min, children: [
          new IconButton(
              onPressed: () => mute(true),
              icon: new Icon(Icons.star_border),
              color: Colors.redAccent),
          new IconButton(
              onPressed: () => play(),
              iconSize: 64.0,
              icon: new Icon(Icons.arrow_left),
              color: Colors.redAccent),
          new IconButton(
              onPressed: isPlaying ? () => pause() : () => play(),
              iconSize: 64.0,
              icon: (isPlaying ? Icon(Icons.pause_circle_filled) : Icon(Icons.play_circle_filled)),
              color: Colors.redAccent),
          new IconButton(
              onPressed: () => nextSong(),
              iconSize: 64.0,
              icon: new Icon(Icons.arrow_right),
              color: Colors.redAccent),
          new IconButton(
              onPressed: () => mute(false),
              icon: new Icon(Icons.queue_music),
              color: Colors.redAccent),
        ]),

//        new Row(
//          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
//          children: <Widget>[
//            new IconButton(
//                onPressed: () => mute(true),
//                icon: new Icon(Icons.headset_off),
//                color: Colors.cyan),
//            new IconButton(
//                onPressed: () => mute(false),
//                icon: new Icon(Icons.headset),
//                color: Colors.cyan),
//          ],
//        ),
        new Row(mainAxisSize: MainAxisSize.min, children: [
//          new Padding(
//              padding: new EdgeInsets.all(12.0),
//              child: new Stack(children: [
//                new CircularProgressIndicator(
//                    value: 1.0,
//                    valueColor: new AlwaysStoppedAnimation(Colors.grey[300])),
//                new CircularProgressIndicator(
//                  value: position != null && position.inMilliseconds > 0
//                      ? (position?.inMilliseconds?.toDouble() ?? 0.0) /
//                      (duration?.inMilliseconds?.toDouble() ?? 0.0)
//                      : 0.0,
//                  valueColor: new AlwaysStoppedAnimation(Colors.cyan),
//                  backgroundColor: Colors.yellow,
//                ),
//              ])),
//          new Text(
//              position != null
//                  ? "${positionText ?? ''} / ${durationText ?? ''}"
//                  : duration != null ? durationText : '',
//              style: new TextStyle(fontSize: 24.0))
        ])
      ]));
}