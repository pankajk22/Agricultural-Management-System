import 'package:flutter/material.dart';
import 'package:carousel_pro/carousel_pro.dart';
//custom imports
import 'package:market/components/horizontallistview.dart';
void main() {
  runApp(
      new MaterialApp(debugShowCheckedModeBanner: false, home: homescreen()));
}

class homescreen extends StatefulWidget {
  @override
  _homescreenState createState() => _homescreenState();
}

class _homescreenState extends State<homescreen> {
  @override
  Widget build(BuildContext context) {
  Widget imagecarousel=new Container(       //image carousel
    height: 200.0,
    child: new Carousel(
      boxFit: BoxFit.cover,
      images:[
        AssetImage('images/IMG_5243.JPG'),
        AssetImage('images/IMG_5247.JPG'),
        AssetImage('images/IMG_5250.JPG'),
        AssetImage('images/IMG_5251.JPG'),
        AssetImage('images/IMG_5253.JPG'),
      ],
      autoplay: true,
      animationCurve: Curves.fastOutSlowIn,
      animationDuration: Duration(milliseconds: 1000),
      dotSize: 4.0,
      dotColor: Colors.red,
      indicatorBgPadding: 4.0,
    ),
  );
    return Scaffold(
      appBar: new AppBar(
        backgroundColor: (Colors.red),
        title: Text("Agriculture Market"),
        actions: <Widget>[
          new IconButton(icon: Icon(Icons.shopping_cart), onPressed: () {}),
        ],
      ),
      drawer: new Drawer(
        child: new ListView(
          children: <Widget>[
            // header
            new UserAccountsDrawerHeader(
              accountName: Text("Pankaj"),
              accountEmail: Text("example@gmail.com"),
              currentAccountPicture: GestureDetector(
                child: new CircleAvatar(
                  backgroundColor: Colors.white,
                  child: new Icon(
                    Icons.person,
                    color: Colors.red,
                  ),
                ),
              ),
              decoration: new BoxDecoration(
                color: Colors.red,
              ),
            ),
            InkWell(
              onTap: () {},
              child: ListTile(
                title: Text("Home"),
                leading: Icon(Icons.home),
              ),
            ),
            InkWell(
              onTap: () {},
              child: ListTile(
                title: Text("About Me"),
                leading: Icon(Icons.person),
              ),
            ),
            InkWell(
              onTap: () {},
              child: ListTile(
                title: Text("Cart"),
                leading: Icon(Icons.shopping_cart),
              ),
            ),
            InkWell(
              onTap: () {},
              child: ListTile(
                title: Text("Settings"),
                leading: Icon(Icons.settings),
              ),
            ),
            InkWell(
              onTap: () {},
              child: ListTile(
                title: Text("Help"),
                leading: Icon(Icons.help),
              ),
            ),
          ],
        ),
      ),
      body: new ListView(
        children:<Widget>[
          imagecarousel,
          //padding widget 
          new Padding(padding: const EdgeInsets.all(8.0),
          child: new Text('Categories'),),
          //horizontal list view here
          HorizontalList(),
        ]
      ),
    );
  }
}
