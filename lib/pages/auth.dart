import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../backend/auth.dart';

class _RoundedInputField extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final bool obscureText;
  final Widget? suffixIcon;

  const _RoundedInputField({
    required this.controller,
    required this.hintText,
    this.obscureText = false,
    this.suffixIcon,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: obscureText,
      decoration: InputDecoration(
        filled: true,
        fillColor: const Color(0x10000000),
        hintText: hintText,
        hintStyle: GoogleFonts.rubik(color: Color(0xFF8099FF)),
        suffixIcon: suffixIcon,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 14,
        ),
        enabledBorder: OutlineInputBorder(
          borderSide: const BorderSide(color: Color(0xFF8099FF), width: 2.5),
          borderRadius: BorderRadius.circular(12),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: const BorderSide(color: Color(0xFF3F65FF), width: 2.5),
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}

class AuthPage extends StatefulWidget {
  final VoidCallback updateAuth;

  const AuthPage({super.key, required this.updateAuth});

  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  final _loginController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscure = true;
  bool _agreeToTerms = false;
  bool _isAuth = true;

  void _showDialog(String content) {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          child: Container(
            padding: EdgeInsets.all(10),
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/dialog_bg.png'),
                fit: BoxFit.cover,
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Ошибка',
                  style: GoogleFonts.rubik(
                    color: Color(0xFFFF8383),
                    fontSize: 40,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                SizedBox(height: 16),
                Text(
                  content,
                  style: GoogleFonts.rubik(
                    color: Colors.white,
                    fontSize: 30,
                    fontWeight: FontWeight.w300,
                  ),
                ),
                SizedBox(height: 24),
                Align(
                  alignment: Alignment.bottomRight,
                  child: TextButton(
                    onPressed: () => Navigator.pop(context),
                    style: TextButton.styleFrom(
                      foregroundColor: Color(0xFF3F65FF),
                    ),
                    child: Text(
                      'Закрыть',
                      style: GoogleFonts.rubik(fontSize: 20),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _onLogin() async {
    String res = await login(_loginController.text, _passwordController.text);
    if (res == 'ok') {
      widget.updateAuth();
    } else {
      if (!mounted) return;

      _loginController.clear();
      _passwordController.clear();

      _showDialog(res);
    }
  }

  Future<void> _onRegister() async {
    String res = await register(
      _loginController.text,
      _nameController.text,
      _emailController.text,
      _passwordController.text,
    );
    if (res == 'ok') {
      widget.updateAuth();
    } else {
      if (!mounted) return;

      _loginController.clear();
      _nameController.clear();
      _emailController.clear();
      _passwordController.clear();

      _showDialog(res);
    }
  }

  void _onTapSignUp() {
    setState(() {
      _isAuth = false;
    });
  }

  void _onTapSignIn() {
    setState(() {
      _isAuth = true;
    });
  }

  Widget _loginPage(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/start_page_bg.png"),
            fit: BoxFit.cover,
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 95),
              Image.asset('assets/logo.png', width: 80, height: 80),
              const SizedBox(height: 30),
              const Text(
                'Авторизация',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF8099FF),
                ),
              ),
              const SizedBox(height: 25),
              // Login
              _RoundedInputField(
                controller: _loginController,
                hintText: 'Логин',
              ),
              const SizedBox(height: 15),
              // Password
              _RoundedInputField(
                controller: _passwordController,
                hintText: 'Пароль',
                obscureText: _obscure,
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscure ? Icons.visibility_off : Icons.visibility,
                    color: Colors.grey,
                  ),
                  onPressed: () => setState(() => _obscure = !_obscure),
                ),
              ),
              const SizedBox(height: 25),
              // Login button
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF3F65FF),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    elevation: 3,
                  ),
                  onPressed: _onLogin,
                  child: const Text(
                    'Войти',
                    style: TextStyle(fontSize: 16, color: Colors.white),
                  ),
                ),
              ),
              const SizedBox(height: 25),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text('Нет аккаунта? '),
                  GestureDetector(
                    onTap: _onTapSignUp,
                    child: const Text(
                      'Зарегистрируйтесь',
                      style: TextStyle(
                        color: Color(0xFF3F65FF),
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _registerPage(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/start_page_bg.png"),
            fit: BoxFit.cover,
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 55),
              Image.asset('assets/logo.png', width: 80, height: 80),
              const SizedBox(height: 30),
              const Text(
                'Регистрация',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF8099FF),
                ),
              ),
              const SizedBox(height: 12),
              Text(
                'Добро пожаловать в Serenify! Удобный способ записаться к врачу, получать рекомендации и следить за своим ментальным здоровьем. Всё в одном месте — просто, быстро и надёжно.',
                textAlign: TextAlign.center,
                style: GoogleFonts.rubik(color: Colors.grey, fontSize: 14),
              ),
              const SizedBox(height: 28),
              // Login
              _RoundedInputField(
                controller: _loginController,
                hintText: 'Логин',
              ),
              const SizedBox(height: 15),
              // Name
              _RoundedInputField(controller: _nameController, hintText: 'ФИО'),
              const SizedBox(height: 15),
              // Email
              _RoundedInputField(
                controller: _emailController,
                hintText: 'Почта',
              ),
              const SizedBox(height: 15),
              // Password
              _RoundedInputField(
                controller: _passwordController,
                hintText: 'Пароль',
                obscureText: _obscure,
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscure ? Icons.visibility_off : Icons.visibility,
                    color: Colors.grey,
                  ),
                  onPressed: () => setState(() => _obscure = !_obscure),
                ),
              ),
              const SizedBox(height: 16),
              // Terms checkbox
              Row(
                children: [
                  Checkbox(
                    value: _agreeToTerms,
                    onChanged: (v) =>
                        setState(() => _agreeToTerms = v ?? false),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(4),
                    ),
                    checkColor: Colors.white,
                    fillColor: WidgetStateProperty.resolveWith<Color>((
                      Set<WidgetState> states,
                    ) {
                      if (states.contains(WidgetState.selected)) {
                        return Color(0xFF3F65FF);
                      }
                      return Colors.transparent;
                    }),
                  ),
                  Expanded(
                    child: Text.rich(
                      TextSpan(
                        text: "Я согласен с ",
                        style: const TextStyle(color: Colors.grey, fontSize: 13),
                        children: [
                          TextSpan(
                            text: "условиями обслуживания",
                            style: GoogleFonts.rubik(color: const Color(0xFF3F65FF)),
                          ),
                          const TextSpan(text: " и "),
                          TextSpan(
                            text: "приватной политикой",
                            style: GoogleFonts.rubik(color: const Color(0xFF3F65FF)),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              // Create Account Button
              ElevatedButton(
                onPressed: _agreeToTerms ? _onRegister : null,
                style: ButtonStyle(
                  backgroundColor: WidgetStateProperty.resolveWith<Color>((
                    Set<WidgetState> states,
                  ) {
                    if (states.contains(WidgetState.disabled)) {
                      return Color(0xFF323E6D);
                    }
                    return const Color(0xFF3F65FF);
                  }),
                  minimumSize: WidgetStateProperty.all<Size>(
                    Size(double.infinity, 54),
                  ),
                  shape: WidgetStateProperty.all<OutlinedBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                  ),
                ),
                child: Text(
                  "Создать аккаунт",
                  style: _agreeToTerms
                      ? GoogleFonts.rubik(fontSize: 16, color: Color(0xFFA3B5FF))
                      : GoogleFonts.rubik(fontSize: 16, color: Color(0xFF202741)),
                ),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text('Вы уже имеете аккаунт? '),
                  GestureDetector(
                    onTap: _onTapSignIn,
                    child: Text(
                      'Войти',
                      style: GoogleFonts.rubik(
                        color: Color(0xFF3F65FF),
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return _isAuth ? _loginPage(context) : _registerPage(context);
  }
}
