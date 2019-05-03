import inputbox


class WrongStartingPointException(Exception):
    def handling(self):
        code = inputbox.display_input_box(1280, 1024, 'Wrong exit! Enter to continue...')
        return code


class WrongInputException(Exception):
    def handling(self):
        code = int(inputbox.display_input_box(400, 400, 'Wrong input, enter again'))
        return code