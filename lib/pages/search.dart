import 'package:flutter/material.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage>
    with TickerProviderStateMixin {
  String selectedDoctor = 'Др. Айжан Каримова';

  final List<Map<String, dynamic>> doctors = [
    {
      'name': 'Др. Айжан Каримова',
      'specialty': 'Психотерапевт',
      'experience': '8 лет',
      'rating': 4.9,
      'price': '15 000 ₸ / сеанс',
      'clinic': 'Serenity Clinic',
      'address': 'ул. Сатпаева, 27, Алматы',
      'schedule': {
        'Пн': '09:00–18:00',
        'Вт': '09:00–18:00',
        'Ср': '09:00–18:00',
        'Чт': '09:00–18:00',
        'Пт': '09:00–18:00',
      },
      'photo': 'assets/doctor_1.jpg',
    },
    {
      'name': 'Др. Наурыз Хайзенберг',
      'specialty': 'Психиатр',
      'experience': '5 лет',
      'rating': 4.9,
      'price': '17 000 ₸ / сеанс',
      'clinic': 'Serenity Clinic',
      'address': 'ул. Толе би, 45, Алматы',
      'schedule': {
        'Пн': '09:00–18:00',
        'Вт': '09:00–18:00',
        'Ср': '09:00–18:00',
        'Чт': '09:00–18:00',
        'Пт': '09:00–18:00',
      },
      'photo': 'assets/doctor_2.jpg',
    },
    {
      'name': 'Др. Гульмира Ким',
      'specialty': 'Невропсихолог',
      'experience': '10 лет',
      'rating': 4.9,
      'price': '12 000 ₸ / сеанс',
      'clinic': 'Serenity Clinic',
      'address': 'ул. Абая, 125, Алматы',
      'schedule': {
        'Пн': '09:00–18:00',
        'Вт': '09:00–18:00',
        'Ср': '09:00–18:00',
        'Чт': '09:00–18:00',
        'Пт': '09:00–18:00',
      },
      'photo': 'assets/doctor_3.jpg',
    },
  ];

  Map<String, bool> expanded = {};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0F152F), Color(0xFF384681)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Dropdown выбора врача
                Container(
                  padding:
                  const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: const Color(0xFF425397),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      dropdownColor: const Color(0xFF384681),
                      value: selectedDoctor,
                      isExpanded: true,
                      iconEnabledColor: Colors.white,
                      items: doctors.map((doc) {
                        return DropdownMenuItem<String>(
                          value: doc['name'],
                          child: Text(
                            doc['name'],
                            style: const TextStyle(color: Colors.white),
                          ),
                        );
                      }).toList(),
                      onChanged: (value) {
                        if (value != null) setState(() => selectedDoctor = value);
                      },
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Expanded(
                  child: ListView.builder(
                    itemCount: doctors.length,
                    itemBuilder: (context, index) {
                      final doc = doctors[index];
                      final isExpanded = expanded[doc['name']] ?? false;

                      return GestureDetector(
                        onTap: () {
                          setState(() {
                            expanded[doc['name']] =
                            !(expanded[doc['name']] ?? false);
                          });
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                          margin: const EdgeInsets.only(bottom: 12),
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: const Color(0xFF425397).withValues(alpha: 0.3),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                                color: const Color(0xFF597AFF), width: 1),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withValues(alpha: 0.25),
                                blurRadius: 8,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          child: AnimatedSize(
                            duration: const Duration(milliseconds: 400),
                            curve: Curves.easeInOut,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    CircleAvatar(
                                      radius: 26,
                                      backgroundImage:
                                      AssetImage(doc['photo']),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            doc['name'],
                                            style: const TextStyle(
                                              fontWeight: FontWeight.w600,
                                              fontSize: 16,
                                              color: Colors.white,
                                            ),
                                          ),
                                          Text(
                                            doc['specialty'],
                                            style: const TextStyle(
                                                color: Color(0xFFB8C0FF)),
                                          ),
                                        ],
                                      ),
                                    ),
                                    AnimatedRotation(
                                      turns: isExpanded ? 0.5 : 0,
                                      duration:
                                      const Duration(milliseconds: 300),
                                      child: const Icon(Icons.expand_more,
                                          color: Colors.white),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  children: [
                                    Text(doc['experience'],
                                        style: const TextStyle(
                                            color: Colors.white70)),
                                    const SizedBox(width: 8),
                                    const Icon(Icons.star,
                                        color: Colors.amber, size: 16),
                                    Text(doc['rating'].toString(),
                                        style: const TextStyle(
                                            color: Colors.white70)),
                                    const SizedBox(width: 8),
                                    Text(doc['price'],
                                        style: const TextStyle(
                                            color: Colors.white70)),
                                  ],
                                ),

                                // Раскрывающаяся часть
                                AnimatedCrossFade(
                                  duration: const Duration(milliseconds: 400),
                                  firstChild: const SizedBox.shrink(),
                                  secondChild: Padding(
                                    padding: const EdgeInsets.only(top: 12),
                                    child: Column(
                                      crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          doc['clinic'],
                                          style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.w500),
                                        ),
                                        Text(
                                          doc['address'],
                                          style: const TextStyle(
                                              color: Color(0xFFB8C0FF)),
                                        ),
                                        const SizedBox(height: 12),
                                        Container(
                                          decoration: BoxDecoration(
                                            color: const Color(0xFF384681),
                                            borderRadius:
                                            BorderRadius.circular(12),
                                          ),
                                          padding: const EdgeInsets.all(12),
                                          child: Column(
                                            children: doc['schedule']
                                                .entries
                                                .map<Widget>((entry) {
                                              return Padding(
                                                padding:
                                                const EdgeInsets.symmetric(
                                                    vertical: 4),
                                                child: Row(
                                                  mainAxisAlignment:
                                                  MainAxisAlignment
                                                      .spaceBetween,
                                                  children: [
                                                    Text(entry.key,
                                                        style: const TextStyle(
                                                            color:
                                                            Colors.white70)),
                                                    Text(entry.value,
                                                        style: const TextStyle(
                                                            color:
                                                            Colors.white70)),
                                                  ],
                                                ),
                                              );
                                            }).toList(),
                                          ),
                                        ),
                                        const SizedBox(height: 12),
                                        SizedBox(
                                          width: double.infinity,
                                          child: ElevatedButton(
                                            onPressed: () {},
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor:
                                              const Color(0xFF597AFF),
                                              shape:
                                              RoundedRectangleBorder(
                                                borderRadius:
                                                BorderRadius.circular(12),
                                              ),
                                              padding:
                                              const EdgeInsets.symmetric(
                                                  vertical: 12),
                                            ),
                                            child: const Text(
                                              'Записаться',
                                              style: TextStyle(
                                                  fontSize: 16,
                                                  fontWeight: FontWeight.w600),
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  crossFadeState: isExpanded
                                      ? CrossFadeState.showSecond
                                      : CrossFadeState.showFirst,
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}