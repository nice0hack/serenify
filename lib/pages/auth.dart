import 'package:flutter/material.dart';

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
        fillColor: const Color(0xFFF3F5F9),
        hintText: hintText,
        hintStyle: const TextStyle(color: Colors.black45),
        suffixIcon: suffixIcon,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 14,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
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

  Future<void> _onLogin() async {
    await login(_loginController.text, _passwordController.text);
    widget.updateAuth();
  }

  Future<void> _onRegister() async {
    await register(
      _loginController.text,
      _nameController.text,
      _emailController.text,
      _passwordController.text,
    );
    widget.updateAuth();
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
      backgroundColor: Theme.of(context).colorScheme.surface,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Icon(Icons.waving_hand, size: 80, color: Colors.amber),
              const SizedBox(height: 20),
              const Text(
                'Авторизация',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF2046F7),
                ),
              ),
              const SizedBox(height: 50),
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
                    backgroundColor: const Color(0xFF2046F7),
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
                        color: Color(0xFF2046F7),
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
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 32),
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: const Color(0xFFE8ECFF),
                  borderRadius: BorderRadius.circular(24),
                ),
                child: const Text("👋", style: TextStyle(fontSize: 36)),
              ),
              const SizedBox(height: 24),
              const Text(
                "Регистрация",
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1E2C62),
                ),
              ),
              const SizedBox(height: 12),
              const Text(
                'Добро пожаловать в KazMed! Удобный способ записаться к врачу, получать рекомендации и следить за своим здоровьем. Всё в одном месте — просто, быстро и надёжно.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey, fontSize: 14),
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
                  ),
                  const Expanded(
                    child: Text.rich(
                      TextSpan(
                        text: "Я согласен с ",
                        style: TextStyle(color: Colors.grey, fontSize: 13),
                        children: [
                          TextSpan(
                            text: "условиями обслуживания",
                            style: TextStyle(color: Colors.blue),
                          ),
                          TextSpan(text: " и "),
                          TextSpan(
                            text: "приватной политикой",
                            style: TextStyle(color: Colors.blue),
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
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF3B5AFB),
                  minimumSize: const Size(double.infinity, 54),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                child: const Text(
                  "Создать аккаунт",
                  style: TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text('Вы уже имеете аккаунт? '),
                  GestureDetector(
                    onTap: _onTapSignIn,
                    child: const Text(
                      'Войти',
                      style: TextStyle(
                        color: Color(0xFF2046F7),
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
