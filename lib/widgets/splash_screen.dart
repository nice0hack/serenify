import 'dart:async';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class SerenifySplashScreen extends StatefulWidget {
  final int loadingTime;
  final Widget? page;

  const SerenifySplashScreen({super.key, this.loadingTime = 3000, this.page});

  @override
  State<SerenifySplashScreen> createState() => _SerenifySplashScreenState();
}

class _SerenifySplashScreenState extends State<SerenifySplashScreen> {
  bool _visible = false;

  Widget _getSplashScreen() {
    final size = MediaQuery.sizeOf(context);

    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset(
            'assets/start_page_bg.png',
            fit: BoxFit.cover,
            width: size.width,
            height: size.height,
          ),
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Image.asset(
                  'assets/logo.png',
                  width: size.width * 0.35,
                  height: size.width * 0.35,
                ),
                const SizedBox(height: 10),
                Text(
                  'Serenify',
                  style: GoogleFonts.rubik(
                    fontSize: 70,
                    fontWeight: FontWeight.w700,
                    color: const Color(0xFFA3B4FE),
                    letterSpacing: 1.1,
                  ),
                ),
              ],
            ),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 25),
              child: Text(
                'Сделано GitGoodTeam',
                style: GoogleFonts.rubik(
                  color: Color(0xFF202A56),
                  fontWeight: FontWeight.bold,
                  fontSize: 12,
                  letterSpacing: 0.3,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void initState() {
    super.initState();

    Timer(Duration(milliseconds: widget.loadingTime), () {
      if (mounted) {
        setState(() {
          _visible = true;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 700),
        switchInCurve: Curves.easeInOut,
        switchOutCurve: Curves.easeInOut,
        transitionBuilder: (Widget child, Animation<double> animation) {
          return FadeTransition(opacity: animation, child: child);
        },
        child: _visible && widget.page != null
            ? widget.page!
            : _getSplashScreen(),
      ),
    );
  }
}
