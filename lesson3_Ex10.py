class TestExample:
    def test_check_phrase(self):
        phrase = input("Set a phrase: ")
        a = len(phrase)
        expected_sum = 15
        assert a < expected_sum, f"Во фразе: '{phrase}' больше или равно {expected_sum} символов"