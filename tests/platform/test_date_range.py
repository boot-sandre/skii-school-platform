import unittest

from skii.platform.models.agent import TeacherAgent
from skii.platform.models.event import LessonEvent
from skii.platform.entities import DatetimeRangeEntity, DatetimeRange
from datetime import datetime, timedelta, UTC

from tests.testcase import SkiiControllerTestCase


class TestDatetimeRange(unittest.TestCase):
    def test_valid_datetime_range(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        self.assertEqual(datetime_range.start, start)
        self.assertEqual(datetime_range.stop, stop)

    def test_invalid_datetime_range(self):
        start = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        with self.assertRaises(ValueError):
            DatetimeRange(start, stop)

    def test_str_representation(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        expected_str = f"{start} - {stop} so {round((stop - start).seconds / 60)} minutes"
        self.assertEqual(str(datetime_range), expected_str)

    def test_add_timedelta(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        added_datetime_range = datetime_range + timedelta(hours=1)

        expected_start = start + timedelta(hours=1)
        expected_stop = stop + timedelta(hours=1)

        self.assertEqual(added_datetime_range.start, expected_start)
        self.assertEqual(added_datetime_range.stop, expected_stop)

    def test_hour_later(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        later_datetime_range = datetime_range.hour_later()

        expected_start = start + timedelta(hours=1)
        expected_stop = stop + timedelta(hours=1)

        self.assertEqual(later_datetime_range.start, expected_start)
        self.assertEqual(later_datetime_range.stop, expected_stop)

    def test_delta(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 12, 30, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        expected_delta = timedelta(hours=4, minutes=30)

        self.assertEqual(datetime_range.delta, expected_delta)

    def test_overlaps(self):
        datetime_range1 = DatetimeRange(
            datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        )
        datetime_range2 = DatetimeRange(
            datetime(2023, 1, 1, 10, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 14, 0, tzinfo=UTC)
        )
        datetime_range3 = DatetimeRange(
            datetime(2023, 1, 1, 14, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 16, 0, tzinfo=UTC)
        )

        self.assertTrue(datetime_range1.overlaps(datetime_range2))
        self.assertFalse(datetime_range1.overlaps(datetime_range3))

    def test_starts_before(self):
        datetime_range1 = DatetimeRange(
            datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        )
        datetime_range2 = DatetimeRange(
            datetime(2023, 1, 1, 10, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 14, 0, tzinfo=UTC)
        )
        datetime_range3 = DatetimeRange(
            datetime(2023, 1, 1, 12, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 16, 0, tzinfo=UTC)
        )

        self.assertTrue(datetime_range1.starts_before(datetime_range2))
        self.assertFalse(datetime_range3.starts_before(datetime_range2))

    def test_range_generation(self):
        start = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop = datetime(2023, 1, 1, 9, 0, tzinfo=UTC)
        datetime_range = DatetimeRange(start, stop)

        step = timedelta(minutes=15)
        expected_datetimes = [
            datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            datetime(2023, 1, 1, 8, 15, tzinfo=UTC),
            datetime(2023, 1, 1, 8, 30, tzinfo=UTC),
            datetime(2023, 1, 1, 8, 45, tzinfo=UTC),
        ]

        generated_datetimes = list(datetime_range.range(step))

        self.assertEqual(generated_datetimes, expected_datetimes)


class TestTimeRangeEntity(unittest.TestCase):
    """We want to unittest DatetimeRangeEntity, but it's an abstract model.

    So we need to use a child class of DatetimeRangeEntity like LessonEvent.
    """

    _model_class: DatetimeRangeEntity = LessonEvent

    def test_datetime_range_property(self):
        # Create a DatetimeRangeEntity instance with specific start and stop times.
        start_time = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop_time = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        time_range_entity = self._model_class(start=start_time, stop=stop_time)

        # Check if the datetime_range property correctly creates a DatetimeRange instance.
        expected_datetime_range = DatetimeRange(start=start_time, stop=stop_time)
        self.assertEqual(time_range_entity.datetime_range, expected_datetime_range)

    def test_datetime_range_property_setter(self):
        # Create a DatetimeRangeEntity instance with initial start and stop times.
        start_time = datetime(2023, 1, 1, 8, 0, tzinfo=UTC)
        stop_time = datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        time_range_entity = self._model_class(start=start_time, stop=stop_time)

        # Update the datetime_range property using a DatetimeRange instance.
        new_datetime_range = DatetimeRange(
            start=datetime(2023, 1, 1, 9, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 13, 0, tzinfo=UTC)
        )
        time_range_entity.datetime_range = new_datetime_range

        # Check if the start and stop times have been updated correctly.
        self.assertEqual(time_range_entity.start, new_datetime_range.start)
        self.assertEqual(time_range_entity.stop, new_datetime_range.stop)

    def test_new_in_datetime_range_method(self):
        # Create a DatetimeRange instance.
        datetime_range = DatetimeRange(
            start=datetime(
                2023, 1, 1, 8, 0, tzinfo=UTC),
            stop=datetime(
                2023, 1, 1, 12, 0, tzinfo=UTC)
        )

        # Create a new DatetimeRangeEntity instance using the new_in_datetime_range method.
        time_range_entity = self._model_class.new_in_datetime_range(datetime_range)

        # Check if the start and stop times of the new instance match the DatetimeRange.
        self.assertEqual(time_range_entity.start, datetime_range.start)
        self.assertEqual(time_range_entity.stop, datetime_range.stop)


class TestTimeRangeManager(SkiiControllerTestCase):
    _model_class: DatetimeRangeEntity = LessonEvent
    _teacher: TeacherAgent = None

    def setUp(self) -> None:
        self._teacher = self.get_factory_instance("teacher", "create")
        # Create test objects with time ranges
        self.datetime_range1 = DatetimeRange(
            start=datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 12, 0, tzinfo=UTC)
        )
        self.datetime_range2 = DatetimeRange(
            start=datetime(2023, 1, 1, 10, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 14, 0, tzinfo=UTC)
        )
        self.datetime_range3 = DatetimeRange(
            start=datetime(2023, 1, 1, 14, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 16, 0, tzinfo=UTC)
        )

        self._model_class.objects.create(
            start=self.datetime_range1.start,
            stop=self.datetime_range1.stop,
            teacher=self._teacher,
        )
        self._model_class.objects.create(
            start=self.datetime_range2.start,
            stop=self.datetime_range2.stop,
            teacher=self._teacher,
        )
        self._model_class.objects.create(
            start=self.datetime_range3.start,
            stop=self.datetime_range3.stop,
            teacher=self._teacher,
        )

    def test_in_range(self):
        # Test filtering objects within a DatetimeRange
        filter_range = DatetimeRange(
            start=datetime(2023, 1, 1, 8, 0, tzinfo=UTC),
            stop=datetime(2023, 1, 1, 14, 0, tzinfo=UTC),
        )
        filtered_objects = self._model_class.objects.in_range(filter_range)
        self.assertEqual(len(filtered_objects), 2)
        self.assertIn(filter_range.start, [obj.start for obj in filtered_objects])
        self.assertIn(filter_range.start, [obj.start for obj in filtered_objects])

