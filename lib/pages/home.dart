import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const _HomePageState(),
    );
  }
}

class _HomePageState extends StatelessWidget {
  const _HomePageState({super.key});

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
                    const Text(
                      "Привет, Илья!",
                      style: TextStyle(
                        color: Color(0xFFBFD9FF),
                        fontSize: 18,
                        fontWeight: FontWeight.w500,
                      ),
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

class _DoctorCard extends StatelessWidget {
  final Color color;
  final String imagePath;


  const _DoctorCard({
    required this.color,
    required this.imagePath,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      height: 150,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: Image.asset(
              imagePath,
              width: 140,
              height: 140,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(height: 8),

        ],
      ),
    );
  }
}