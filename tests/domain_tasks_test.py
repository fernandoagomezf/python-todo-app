import unittest
import sys
import os
from datetime import date 
from datetime import timedelta
from datetime import datetime


print(sys.path)

from domain.tasks import Task, TaskStatus, TaskPriority

class TestTask(unittest.TestCase):
    def setUp(self):
        self.subject = "Test Task"
        self.task = Task(self.subject)

    def test_initialization(self):
        self.assertEqual(self.task.get_subject(), self.subject)
        self.assertEqual(self.task.get_status(), TaskStatus.PENDING.value)
        self.assertEqual(self.task.get_priority(), TaskPriority.NORMAL.value)
        self.assertEqual(self.task.get_progress(), 0.0)
        self.assertIsInstance(self.task.get_code(), str)
        self.assertIsInstance(self.task.get_due_date(), date)
        self.assertEqual(self.task.get_notes(), "")

    def test_empty_subject_raises(self):
        with self.assertRaises(ValueError):
            Task("")

    def test_update_content(self):
        new_subject = "Updated Task"
        new_notes = "Some notes"
        self.task.update_content(subject=new_subject, notes=new_notes)
        self.assertEqual(self.task.get_subject(), new_subject)
        self.assertEqual(self.task.get_notes(), new_notes)

    def test_update_content_empty_subject_raises(self):
        with self.assertRaises(ValueError):
            self.task.update_content(subject="")

    def test_move_due_date_by_days(self):
        old_due = self.task.get_due_date()
        self.task.move_due_date(days=2)
        self.assertEqual(self.task.get_due_date(), old_due + timedelta(days=2))

    def test_move_due_date_to_new_date(self):
        new_date = datetime.now().date() + timedelta(days=5)
        self.task.move_due_date(new_date=new_date)
        self.assertEqual(self.task.get_due_date(), new_date)

    def test_move_due_date_invalid(self):
        with self.assertRaises(ValueError):
            self.task.move_due_date()
        with self.assertRaises(ValueError):
            self.task.move_due_date(new_date=datetime.now().date() - timedelta(days=1))

    def test_report_progress(self):
        self.task.report_progress(50.0)
        self.assertEqual(self.task.get_progress(), 50.0)
        self.assertEqual(self.task.get_status(), TaskStatus.IN_PROGRESS.value)
        self.task.report_progress(0.0)
        self.assertEqual(self.task.get_status(), TaskStatus.PENDING.value)
        self.task.report_progress(100.0)
        self.assertEqual(self.task.get_status(), TaskStatus.COMPLETED.value)

    def test_report_progress_invalid(self):
        with self.assertRaises(ValueError):
            self.task.report_progress(-1.0)
        with self.assertRaises(ValueError):
            self.task.report_progress(101.0)

    def test_complete(self):
        self.task.complete()
        self.assertEqual(self.task.get_progress(), 100.0)
        self.assertEqual(self.task.get_status(), TaskStatus.COMPLETED.value)

    def test_cancel(self):
        self.task.cancel()
        self.assertEqual(self.task.get_status(), TaskStatus.CANCELLED.value)
        self.assertEqual(self.task.get_progress(), 0.0)

    def test_promote_and_demote(self):
        self.task.promote()
        self.assertEqual(self.task.get_priority(), TaskPriority.HIGH.value)
        self.task.demote()
        self.assertEqual(self.task.get_priority(), TaskPriority.NORMAL.value)
        self.task.demote()
        self.assertEqual(self.task.get_priority(), TaskPriority.LOW.value)
        self.task.promote()
        self.assertEqual(self.task.get_priority(), TaskPriority.NORMAL.value)

if __name__ == "__main__":
    unittest.main()
