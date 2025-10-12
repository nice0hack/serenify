import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_calendar/calendar.dart';

class MeetingDataSource extends CalendarDataSource {
  MeetingDataSource(List<Meeting> source) {
    appointments = source;
  }

  @override
  DateTime getStartTime(int index) =>
      (appointments![index] as Meeting).from;

  @override
  DateTime getEndTime(int index) =>
      (appointments![index] as Meeting).to;

  @override
  String getSubject(int index) =>
      (appointments![index] as Meeting).eventName;

  @override
  Color getColor(int index) =>
      (appointments![index] as Meeting).background;

  @override
  bool isAllDay(int index) =>
      (appointments![index] as Meeting).isAllDay;
}

class Meeting {
  const Meeting(
      this.eventName,
      this.from,
      this.to,
      this.background,
      this.isAllDay,
      );

  final String eventName;
  final DateTime from;
  final DateTime to;
  final Color background;
  final bool isAllDay;
}

class CalendarPage extends StatefulWidget {
  final String _title = 'Календарь';

  const CalendarPage({super.key});

  @override
  State<CalendarPage> createState() => _CalendarPageState();
}

class _CalendarPageState extends State<CalendarPage> {
  List<Meeting> _getDataSource() {
    final today = DateTime.now();
    final startTime = DateTime(today.year, today.month, today.day, 9);
    final endTime = startTime.add(const Duration(hours: 2));

    return [
      Meeting(
        'Прием пациента',
        startTime,
        endTime,
        const Color(0xFF8099FF),
        false,
      ),
      Meeting(
        'Консультация',
        startTime.add(const Duration(days: 1)),
        endTime.add(const Duration(days: 1)),
        const Color(0xFF597AFF),
        false,
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text(
          widget._title,
          style: const TextStyle(
            fontWeight: FontWeight.w600,
            fontSize: 20,
            color: Color(0xFF8099FF),
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      body: DecoratedBox(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0F152F), Color(0xFF384681)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white.withValues(alpha: 0.15)),
                ),
                child: SfCalendar(
                  view: CalendarView.month,
                  todayHighlightColor: const Color(0xFF8099FF),
                  backgroundColor: Colors.transparent,
                  headerStyle: const CalendarHeaderStyle(
                    textAlign: TextAlign.center,
                    textStyle: TextStyle(
                      color: Color(0xFF8099FF),
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  viewHeaderStyle: const ViewHeaderStyle(
                    dayTextStyle: TextStyle(
                      color: Colors.white70,
                      fontSize: 13,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  monthViewSettings: const MonthViewSettings(
                    appointmentDisplayMode:
                    MonthAppointmentDisplayMode.appointment,
                    showAgenda: true,
                    agendaViewHeight: 150,
                    agendaItemHeight: 52,
                    monthCellStyle: MonthCellStyle(
                      textStyle: TextStyle(color: Colors.white),
                      leadingDatesTextStyle:
                      TextStyle(color: Colors.white38, fontSize: 12),
                      trailingDatesTextStyle:
                      TextStyle(color: Colors.white38, fontSize: 12),
                    ),
                  ),
                  dataSource: MeetingDataSource(_getDataSource()),
                  appointmentBuilder: (context, details) {
                    final meeting = details.appointments.first as Meeting;
                    return AnimatedContainer(
                      duration: const Duration(milliseconds: 250),
                      curve: Curves.easeInOut,
                      decoration: BoxDecoration(
                        color: meeting.background.withValues(alpha: 0.3),
                        border: Border.all(
                          color: meeting.background.withValues(alpha: 0.8),
                          width: 1,
                        ),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 4,
                      ),
                      child: Center(
                        child: Text(
                          meeting.eventName,
                          style: TextStyle(
                            color: meeting.background,
                            fontWeight: FontWeight.w600,
                            fontSize: 12,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    );
                  },
                  selectionDecoration: BoxDecoration(
                    color: const Color(0x338099FF),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0x668099FF)),
                  ),
                  todayTextStyle: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}