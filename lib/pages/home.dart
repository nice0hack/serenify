import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../secure_storage.dart';

class _DoctorCard extends StatelessWidget {
  final Color color;
  final String imagePath;

  const _DoctorCard({required this.color, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      height: 150,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(10),
      ),
      clipBehavior: Clip.antiAlias,
      child: Image.asset(imagePath, fit: BoxFit.fill),
    );
  }
}

class TipItem {
  final String imagePath;
  final Color? backgroundColor;
  final String? title;

  const TipItem({required this.imagePath, this.backgroundColor, this.title});
}

class TipCard extends StatelessWidget {
  final TipItem tip;

  const TipCard({super.key, required this.tip});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 260,
      decoration: BoxDecoration(
        color: tip.backgroundColor ?? Colors.transparent,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.15),
            blurRadius: 6,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      clipBehavior: Clip.antiAlias,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(20),
        child: Image.asset(
          tip.imagePath,
          fit: BoxFit.fill,
          alignment: Alignment.topLeft,
        ),
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<TipItem> tips = const [
    TipItem(imagePath: "assets/tip_1.png"),
    TipItem(imagePath: "assets/tip_2.png"),
    TipItem(imagePath: "assets/tip_3.png"),
    TipItem(imagePath: "assets/tip_4.png"),
  ];

  Future<String?> _getName() async {
    return storage.read(key: 'name');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0E1632),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    FutureBuilder<String?>(
                      future: _getName(),
                      builder: (context, snapshot) {
                        return Text(
                          "Привет, ${snapshot.data}!",
                          style: TextStyle(
                            color: Color(0xFFBFD9FF),
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                          ),
                        );
                      },
                    ),
                    IconButton(
                      icon: const Icon(
                        Icons.notifications_none,
                        color: Colors.white,
                      ),
                      onPressed: () {},
                    ),
                  ],
                ),
              ),
              Stack(
                clipBehavior: Clip.none,
                children: [
                  Container(
                    width: 470,
                    height: 220,
                    decoration: const BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage('assets/water_back.png'),
                      ),
                    ),
                  ),

                  Positioned(
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: Center(
                      child: Container(
                        width: 150,
                        height: 55,
                        decoration: BoxDecoration(
                          color: const Color(0xFF7D8FFF),
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(
                            color: const Color.fromARGB(255, 184, 198, 255),
                            width: 0.5,
                          ),
                          boxShadow: [
                            BoxShadow(
                              color: const Color.fromARGB(
                                255,
                                255,
                                255,
                                255,
                              ).withValues(alpha: 0.6),
                              blurRadius: 8,
                              offset: const Offset(0, 1),
                            ),
                          ],
                        ),
                        child: Center(
                          child: Text(
                            "Поиск",
                            style: GoogleFonts.rubik(
                              color: Colors.white,
                              fontSize: 23,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 50),

              const Padding(
                padding: EdgeInsets.only(left: 20, top: 24, bottom: 12),
                child: Text(
                  "Мы заботимся о вас",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              SizedBox(
                height: 160,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  itemCount: tips.length,
                  separatorBuilder: (_, _) => const SizedBox(width: 16),
                  itemBuilder: (context, index) {
                    return TipCard(tip: tips[index]);
                  },
                ),
              ),
              const Padding(
                padding: EdgeInsets.only(left: 20, top: 24, bottom: 12),
                child: Text(
                  "Они вам помогут",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              SizedBox(
                height: 160,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  children: const [
                    _DoctorCard(
                      color: Color.fromARGB(0, 0, 0, 0),
                      imagePath: "assets/spec_1.png",
                    ),
                    SizedBox(width: 16),
                    _DoctorCard(
                      color: Color.fromARGB(0, 0, 0, 0),
                      imagePath: "assets/spec_2.png",
                    ),
                    SizedBox(width: 16),
                    _DoctorCard(
                      color: Color.fromARGB(0, 0, 0, 0),
                      imagePath: "assets/spec_3.png",
                    ),
                    SizedBox(width: 16),
                    _DoctorCard(
                      color: Color.fromARGB(0, 0, 0, 0),
                      imagePath: "assets/spec_4.png",
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
