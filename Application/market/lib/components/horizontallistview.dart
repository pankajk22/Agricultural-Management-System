import 'package:flutter/material.dart';

class HorizontalList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 80,
      child: ListView(
        scrollDirection: Axis.horizontal,
        children: <Widget>[
          category(
            image_location: 'images/cats/crops.jpg',
            image_caption: 'crops',
          ),
          category(
            image_location: 'images/cats/pulses.jpg',
            image_caption: 'pulses',
          ),
          category(
            image_location: 'images/cats/spices.jpg',
            image_caption: 'spices',
          ),
          category(
            image_location: 'images/cats/seeds.jpg',
            image_caption: 'seeds',
          ),

        ],
      ),
    );
  }
}

class category extends StatelessWidget {
  final String image_location;
  final String image_caption;
  category({this.image_location, this.image_caption});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(2.0),
      child: InkWell(
          onTap: () {},
          child: Container(
            width: 100,
            child: ListTile(
              title: Image.asset(
                image_location,
                width: 100,
                height: 80,
              ),
              subtitle: Text(image_caption),
            ),
          )),
    );
  }
}
