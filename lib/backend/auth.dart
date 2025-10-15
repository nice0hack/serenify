import 'dart:convert';

import 'package:http/http.dart' as http;

import '../constants.dart';
import '../secure_storage.dart';

Future<bool> isAuth() async {
  final token = await storage.read(key: 'access_token');

  final res = await http.get(
    Uri.parse('${Constants.apiBaseUrl}/me/'),
    headers: {'Authorization': 'Bearer $token'},
  );

  if (res.statusCode == 200) {
    final data = jsonDecode(res.body);
    await storage.write(key: 'name', value: data['name']);
    return true;
  } else {
    return false;
  }
}

Future<String> register(
  String login,
  String name,
  String email,
  String password,
) async {
  final res = await http.post(
    Uri.parse('${Constants.apiBaseUrl}/register/'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'login': login,
      'name': name,
      'email': email,
      'password': password,
    }),
  );
  if (res.statusCode == 200) {
    final data = jsonDecode(res.body);
    await storage.write(key: 'access_token', value: data['access_token']);
    await storage.write(key: 'refresh_token', value: data['refresh_token']);

    if (await isAuth()) {
      return 'ok';
    }
    else {
      return 'Ошибка регистрации';
    }
  }
  else if (res.statusCode == 422) {
    return 'Неправильный формат почты';
  }
  else {
    return jsonDecode(res.body)['detail'];
  }
}

Future<String> login(String login, String password) async {
  final res = await http.post(
    Uri.parse('${Constants.apiBaseUrl}/auth/'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'login': login, 'password': password}),
  );
  if (res.statusCode == 200) {
    final data = jsonDecode(res.body);
    await storage.write(key: 'access_token', value: data['access_token']);
    await storage.write(key: 'refresh_token', value: data['refresh_token']);

    if (await isAuth()) {
      return 'ok';
    }
    else {
      return 'Ошибка регистрации';
    }
  } else {
    return jsonDecode(res.body)['detail'];
  }
}
