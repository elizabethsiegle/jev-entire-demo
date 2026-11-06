import unittest
from unittest.mock import Mock

from retry import retry


class RetryTests(unittest.TestCase):
    def test_immediate_success_returns_original_result(self):
        result = object()
        operation = Mock(return_value=result)

        self.assertIs(retry(operation), result)
        operation.assert_called_once_with()

    def test_transient_failures_succeed_within_three_attempts(self):
        for failures in (1, 2):
            with self.subTest(failures=failures):
                result = object()
                operation = Mock(
                    side_effect=[ConnectionError() for _ in range(failures)]
                    + [result]
                )

                self.assertIs(retry(operation), result)
                self.assertEqual(operation.call_count, failures + 1)
                self.assertTrue(all(call.args == () and call.kwargs == {}
                                    for call in operation.call_args_list))

    def test_third_failure_reraises_last_connection_error(self):
        errors = [ConnectionError(str(i)) for i in range(3)]
        operation = Mock(side_effect=errors + [object()])

        with self.assertRaises(ConnectionError) as raised:
            retry(operation)

        self.assertIs(raised.exception, errors[-1])
        self.assertEqual(operation.call_count, 3)

    def test_other_errors_propagate_without_retry(self):
        for failures in (0, 1):
            with self.subTest(prior_connection_failures=failures):
                error = ValueError("operation failed")
                operation = Mock(
                    side_effect=[ConnectionError() for _ in range(failures)]
                    + [error, object()]
                )

                with self.assertRaises(ValueError) as raised:
                    retry(operation)

                self.assertIs(raised.exception, error)
                self.assertEqual(operation.call_count, failures + 1)


if __name__ == "__main__":
    unittest.main()
