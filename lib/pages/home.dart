import 'package:flutter/material.dart';

void main() {
  runApp(const HomePage());
}

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
      backgroundColor: const Color(0xFF0E1632), // Темно-синий фон
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Верхняя панель
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Привет, Никита!",
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

              // Заголовок с фоновым изображением
              Stack(
                clipBehavior: Clip.none,
                children: [
                  // Фон с картинкой
                  Container(
                    width: 470,
                    height: 220,
                    decoration: const BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage('assets/WaterBack.png'),
                      ),
                    ),
                  ),

                  // Кнопка "Поиск" с вырезом снизу
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
                              ).withOpacity(0.6),
                              blurRadius: 8,
                              offset: const Offset(0, 1),
                            ),
                          ],
                        ),
                        child: const Center(
                          child: Text(
                            "Поиск",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 23,
                              fontWeight: FontWeight.w500,
                              fontFamily: "Times New Roman",
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 50),

              // Раздел "Мы заботимся о вас"
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
                height: 140,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  children: [
                    _buildCareCard(Colors.blueAccent),
                    _buildCareCard(Colors.greenAccent),
                    _buildCareCard(Colors.redAccent),
                  ],
                ),
              ),

              // Раздел "Они вам помогут"
              const Padding(
                padding: EdgeInsets.only(left: 20, top: 24, bottom: 12),
                child: Text(
                  "Они вам не помогут",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),

              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    _DoctorCard(
                      color: Color(0xFF708FFF),
                      icon: Icons.favorite,
                      label: "Психотерапевт",
                    ),
                    _DoctorCard(
                      color: Color(0xFFFF6B6B),
                      icon: Icons.favorite,
                      label: "Психолог",
                    ),
                  ],
                ),
              ),

              // тестово чекнуть как работает листинг
              SizedBox(
                height: 30,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  children: [
                    _buildCareCard(Colors.blueAccent),
                    _buildCareCard(Colors.greenAccent),
                    _buildCareCard(Colors.redAccent),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  static Widget _buildCareCard(Color color) {
    return Container(
      width: 120,
      margin: const EdgeInsets.only(right: 16),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(20),
      ),
    );
  }
}

class _DoctorCard extends StatelessWidget {
  final Color color;
  final IconData icon;
  final String label;

  const _DoctorCard({
    required this.color,
    required this.icon,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 140,
      height: 140,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: Colors.white, size: 40),
          const SizedBox(height: 8),
          Text(
            label,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
