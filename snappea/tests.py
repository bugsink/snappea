import unittest
from unittest.mock import patch

from .decorators import shared_task, registry


class TestSharedTaskDecorator(unittest.TestCase):
    @patch('snappea.decorators.get_settings')
    @patch('snappea.decorators.Task.objects.create')
    @patch('snappea.decorators.time_to_logger')
    def test_shared_task_eager_execution(self, mock_time_to_logger, mock_task_create, mock_get_settings):
        mock_get_settings.return_value.TASK_ALWAYS_EAGER = True

        @shared_task
        def sample_task(arg1, arg2):
            return arg1 + arg2

        # Call the task
        sample_task.delay(1, 2)

        # Since TASK_ALWAYS_EAGER is True, the task should be executed immediately
        self.assertEqual(sample_task(1, 2), 3)
        mock_task_create.assert_not_called()

    @patch('snappea.decorators.get_settings')
    @patch('snappea.decorators.Task.objects.create')
    @patch('snappea.decorators.time_to_logger')
    def test_shared_task_delayed_execution(self, mock_time_to_logger, mock_task_create, mock_get_settings):
        mock_get_settings.return_value.TASK_ALWAYS_EAGER = False

        @shared_task
        def sample_task(arg1, arg2):
            return arg1 + arg2

        # Call the task
        sample_task.delay(1, 2)

        # Since TASK_ALWAYS_EAGER is False, it should be delayed and Task should be created
        mock_task_create.assert_called_once_with(
            task_name='snappea.tests.sample_task',
            args='[1, 2]',
            kwargs='{}'
        )

        self.assertEqual(registry['snappea.tests.sample_task'], sample_task)
