import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'package:typicons_flutter/typicons_flutter.dart';

import 'backend/auth.dart';
import 'pages/auth.dart';
import 'pages/calendar.dart';
import 'pages/home.dart';
import 'pages/profile.dart';
import 'pages/search.dart';
import 'widgets/splash_screen.dart';

class SerenifyNavigation extends StatefulWidget {
  const SerenifyNavigation({super.key});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  @override
  State<SerenifyNavigation> createState() => _SerenifyNavigationState();
}

class _SerenifyNavigationState extends State<SerenifyNavigation> {
  final List<Widget> _pages = [
    HomePage(),
    SearchPage(),
    CalendarPage(title: 'calendar'),
    ProfilePage(title: 'profile'),
  ];

  int _selectedIndex = 0;

  late Future<bool> _isAuth;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void updateAuth() {
    setState(() {
      _isAuth = isAuth();
    });
  }

  @override
  void initState() {
    super.initState();
    updateAuth();
  }

  Widget mainContent(BuildContext context) {
    return Container(
      color: Colors.white,
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: _pages[_selectedIndex],
        bottomNavigationBar: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
            ),
            boxShadow: [
              BoxShadow(blurRadius: 20, color: Colors.black.withValues(alpha: .2)),
            ],
          ),
          child: SafeArea(
            child: Container(
              color: Color(0xFFA4AED7),
              padding: EdgeInsets.only(top: 1),
              child: GNav(
                curve: Curves.easeOutExpo,
                rippleColor: Color(0xFF8099FF),
                hoverColor: Color(0xFF8099FF),
                haptic: true,
                tabBorderRadius: 20,
                gap: 5,
                activeColor: Colors.white,
                backgroundColor: Color(0xFF0C1126),
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                duration: Duration(milliseconds: 400),
                tabBackgroundColor: Color(0xFF3F65FF),
                textStyle: GoogleFonts.rubik(color: Colors.white),
                tabs: [
                  GButton(
                    iconSize: _selectedIndex != 0 ? 28 : 25,
                    icon: _selectedIndex == 0
                        ? Icons.home
                        : Icons.home_outlined,
                    text: 'Главная',
                  ),
                  GButton(icon: Icons.search, text: 'Поиск'),
                  GButton(
                    iconSize: 28,
                    icon: _selectedIndex == 2
                        ? Typicons.calendar
                        : Typicons.calendar_outline,
                    text: 'Календарь',
                  ),
                  GButton(
                    iconSize: 29,
                    icon: _selectedIndex == 3
                        ? Typicons.user
                        : Typicons.user_outline,
                    text: 'Профиль',
                  ),
                ],
                selectedIndex: _selectedIndex,
                onTabChange: _onItemTapped,
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _isAuth,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          final isAuth = snapshot.data!;
          if (isAuth) {
            return SerenifySplashScreen(loadingTime: 4500, page: mainContent(context));
          }
          else {
            return SerenifySplashScreen(loadingTime: 4500, page: AuthPage(updateAuth: updateAuth));
          }
        }

        return SerenifySplashScreen(loadingTime: 4500);
      },
    );
  }
}
