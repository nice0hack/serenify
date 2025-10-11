import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

class PageLoader extends StatefulWidget {
  final int loadingTime;
  final Widget? page;

  const PageLoader({super.key, this.loadingTime = 3000, this.page});

  @override
  State<PageLoader> createState() => _PageLoaderState();
}

class _PageLoaderState extends State<PageLoader> {
  bool _visible = false;

  @override
  void initState() {
    super.initState();

    Timer(Duration(seconds: widget.loadingTime), () {
      if (mounted) {
        setState(() {
          _visible = true;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_visible || widget.page == null) {
      return Scaffold(
        backgroundColor: Colors.transparent,
        body: Center(
          child: SvgPicture.asset(
            'assets/page_loader.svg',
            fit: BoxFit.cover,
            colorFilter: null,
          ),
        ),
      );
    } else {
      return widget.page!;
    }
  }
}
