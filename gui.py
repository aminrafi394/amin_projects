import wx
from logic import MathQuiz

class QuizFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 400))

        self.quiz = MathQuiz()
        self.current_question = None
        self.remaining_time = 20

        self.panel = wx.Panel(self)
        self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.farsi_font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Tahoma")

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.build_ui()
        self.Center()
        self.Show()
        self.new_question()

    def build_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.question_label = wx.StaticText(self.panel, label="", style=wx.ALIGN_CENTER)
        self.question_label.SetFont(self.font)
        vbox.Add(self.question_label, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.time_label = wx.StaticText(self.panel, label="20")
        self.time_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(self.time_label, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=5)

        self.answer_input = wx.TextCtrl(self.panel)
        vbox.Add(self.answer_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=50)

        self.submit_btn = wx.Button(self.panel, label="ثبت پاسخ")
        vbox.Add(self.submit_btn, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.feedback_label = wx.StaticText(self.panel, label="")
        self.feedback_label.SetFont(self.farsi_font)
        vbox.Add(self.feedback_label, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.stats_label = wx.StaticText(self.panel, label="")
        self.stats_label.SetFont(self.farsi_font)
        vbox.Add(self.stats_label, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        self.panel.SetSizer(vbox)
        self.submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        self.answer_input.Bind(wx.EVT_TEXT_ENTER, self.on_submit)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def new_question(self):
        self.remaining_time = 20
        self.timer.Start(1000)
        a, op, b = self.quiz.generate_question()
        self.current_question = (a, op, b)
        self.question_label.SetLabel(f"{a} {op} {b} = ?")
        self.answer_input.SetValue("")
        self.feedback_label.SetLabel("")
        self.update_stats()

    def on_timer(self, event):
        self.remaining_time -= 1
        self.time_label.SetLabel(str(self.remaining_time))
        if self.remaining_time == 0:
            self.timer.Stop()
            self.feedback_label.SetLabel("⏰ وقت تمام شد!")
            self.quiz.wrong_count += 1
            self.update_stats()
            wx.CallLater(1500, self.check_continue)

    def on_submit(self, event):
        if not self.current_question:
            return

        self.timer.Stop()
        user_input = self.answer_input.GetValue()
        a, op, b = self.current_question
        correct, correct_answer = self.quiz.check_answer(a, op, b, user_input)

        if correct:
            self.feedback_label.SetLabel("✅ درست بود!")
        else:
            self.feedback_label.SetLabel(f"❌ نادرست. پاسخ صحیح: {correct_answer}")

        self.update_stats()
        wx.CallLater(1500, self.check_continue)

    def update_stats(self):
        correct, wrong, total = self.quiz.get_stats()
        self.stats_label.SetLabel(f"پاسخ‌های درست: {correct}  |  پاسخ‌های نادرست: {wrong}")

    def check_continue(self):
        if self.quiz.total_questions_asked % 5 == 0:
            dlg = wx.MessageDialog(self, "آیا مایل به ادامه هستید؟", "ادامه بازی؟", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result != wx.ID_YES:
                self.Close()
                return
        self.new_question()

    def on_close(self, event):
        correct, wrong, total = self.quiz.get_stats()
        dlg = wx.MessageDialog(
            self,
            f"تعداد پاسخ‌های درست: {correct}\nتعداد پاسخ‌های نادرست: {wrong}\n\nخروج از بازی؟",
            "پایان بازی",
            wx.OK | wx.CANCEL | wx.ICON_INFORMATION
        )
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        else:
            event.Veto()

if __name__ == "__main__":
    app = wx.App(False)
    frame = QuizFrame(None, "بازی ریاضی")
    app.MainLoop()
