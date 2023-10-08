import unittest

from skii.platform.models.agent import TeacherAgent
from skii.platform.models.event import LessonEvent
from skii.platform.entities import DatetimeRangeEntity, DateRange
from datetime import datetime, timedelta, UTC

from tests.testcase import SkiiControllerTestCase


class TestDateRange(unittest.TestCase):
    def test_valid_date_range(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 12, 0)
        date_range = DateRange(start, stop)

        self.assertEqual(date_range.start, start)
        self.assertEqual(date_range.stop, stop)

    def test_invalid_date_range(self):
        start = datetime(2023, 1, 1, 12, 0)
        stop = datetime(2023, 1, 1, 8, 0)  # End before start, should raise ValueError
        with self.assertRaises(ValueError):
            DateRange(start, stop)

    def test_str_representation(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 12, 0)
        date_range = DateRange(start, stop)

        expected_str = f"DateRange({start} - {stop})"
        self.assertEqual(str(date_range), expected_str)

    def test_add_timedelta(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 12, 0)
        date_range = DateRange(start, stop)

        added_date_range = date_range + timedelta(hours=1)

        expected_start = start + timedelta(hours=1)
        expected_stop = stop + timedelta(hours=1)

        self.assertEqual(added_date_range.start, expected_start)
        self.assertEqual(added_date_range.stop, expected_stop)

    def test_hour_later(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 12, 0)
        date_range = DateRange(start, stop)

        later_date_range = date_range.hour_later()

        expected_start = start + timedelta(hours=1)
        expected_stop = stop + timedelta(hours=1)

        self.assertEqual(later_date_range.start, expected_start)
        self.assertEqual(later_date_range.stop, expected_stop)

    def test_duration(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 12, 30)
        date_range = DateRange(start, stop)

        expected_duration = timedelta(hours=4, minutes=30)

        self.assertEqual(date_range.duration, expected_duration)

    def test_overlaps(self):
        date_range1 = DateRange(datetime(2023, 1, 1, 8, 0), datetime(2023, 1, 1, 12, 0))
        date_range2 = DateRange(
            datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 14, 0)
        )
        date_range3 = DateRange(
            datetime(2023, 1, 1, 14, 0), datetime(2023, 1, 1, 16, 0)
        )

        self.assertTrue(date_range1.overlaps(date_range2))
        self.assertFalse(date_range1.overlaps(date_range3))

    def test_starts_before(self):
        date_range1 = DateRange(datetime(2023, 1, 1, 8, 0), datetime(2023, 1, 1, 12, 0))
        date_range2 = DateRange(
            datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 14, 0)
        )
        date_range3 = DateRange(
            datetime(2023, 1, 1, 12, 0), datetime(2023, 1, 1, 16, 0)
        )

        self.assertTrue(date_range1.starts_before(date_range2))
        self.assertFalse(date_range3.starts_before(date_range2))

    def test_range_generation(self):
        start = datetime(2023, 1, 1, 8, 0)
        stop = datetime(2023, 1, 1, 9, 0)
        date_range = DateRange(start, stop)

        step = timedelta(minutes=15)
        expected_datetimes = [
            datetime(2023, 1, 1, 8, 0),
            datetime(2023, 1, 1, 8, 15),
            datetime(2023, 1, 1, 8, 30),
            datetime(2023, 1, 1, 8, 45),
        ]

        generated_datetimes = list(date_range.range(step))

        self.assertEqual(generated_datetimes, expected_datetimes)


class TestTimeRangeEntity(unittest.TestCase):
    """We want to unittest DatetimeRangeEntiry but it's an abstract model.

    So we need to use a child class of DatetimeRangeEntity like LessonEvent.
    """

    _model_class: DatetimeRangeEntity = LessonEvent

    def test_date_range_property(self):
        # Create a DatetimeRangeEntity instance with specific start and stop times.
        start_time = datetime(2023, 1, 1, 8, 0)
        stop_time = datetime(2023, 1, 1, 12, 0)
        time_range_entity = self._model_class(start=start_time, stop=stop_time)

        # Check if the date_range property correctly creates a DateRange instance.
        expected_date_range = DateRange(start=start_time, stop=stop_time)
        self.assertEqual(time_range_entity.date_range, expected_date_range)

    def test_date_range_property_setter(self):
        # Create a DatetimeRangeEntity instance with initial start and stop times.
        start_time = datetime(2023, 1, 1, 8, 0)
        stop_time = datetime(2023, 1, 1, 12, 0)
        time_range_entity = self._model_class(start=start_time, stop=stop_time)

        # Update the date_range property using a DateRange instance.
        new_date_range = DateRange(
            start=datetime(2023, 1, 1, 9, 0), stop=datetime(2023, 1, 1, 13, 0)
        )
        time_range_entity.date_range = new_date_range

        # Check if the start and stop times have been updated correctly.
        self.assertEqual(time_range_entity.start, new_date_range.start)
        self.assertEqual(time_range_entity.stop, new_date_range.stop)

    def test_new_in_date_range_method(self):
        # Create a DateRange instance.
        date_range = DateRange(
            start=datetime(2023, 1, 1, 8, 0), stop=datetime(2023, 1, 1, 12, 0)
        )

        # Create a new DatetimeRangeEntity instance using the new_in_date_range method.
        time_range_entity = self._model_class.new_in_date_range(date_range)

        # Check if the start and stop times of the new instance match the DateRange.
        self.assertEqual(time_range_entity.start, date_range.start)
        self.assertEqual(time_range_entity.stop, date_range.stop)


class TestTimeRangeManager(SkiiControllerTestCase):
    _model_class: DatetimeRangeEntity = LessonEvent
    _teacher: TeacherAgent = None

    def setUp(self) -> None:
        self._teacher = self.get_factory_instance("teacher", "create")
        # Create test objects with time ranges
        self.date_range1 = DateRange(
            start=datetime(2023, 1, 1, 8, 0), stop=datetime(2023, 1, 1, 12, 0)
        )
        self.date_range2 = DateRange(
            start=datetime(2023, 1, 1, 10, 0), stop=datetime(2023, 1, 1, 14, 0)
        )
        self.date_range3 = DateRange(
            start=datetime(2023, 1, 1, 14, 0), stop=datetime(2023, 1, 1, 16, 0)
        )

        self._model_class.objects.create(
            start=self.date_range1.start,
            stop=self.date_range1.stop,
            teacher=self._teacher,
        )
        self._model_class.objects.create(
            start=self.date_range2.start,
            stop=self.date_range2.stop,
            teacher=self._teacher,
        )
        self._model_class.objects.create(
            start=self.date_range3.start,
            stop=self.date_range3.stop,
            teacher=self._teacher,
        )

    def test_in_range(self):
        # Test filtering objects within a DateRange
        filter_range = DateRange(
            start=datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 14, 0, tzinfo=UTC),
        )
        filtered_objects = self._model_class.objects.in_range(filter_range)
        self.assertEqual(len(filtered_objects), 2)
        self.assertIn(filter_range.start, [obj.start for obj in filtered_objects])
        self.assertIn(filter_range.start, [obj.start for obj in filtered_objects])

