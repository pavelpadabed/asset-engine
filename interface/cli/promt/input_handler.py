class InputHandler:
    def confirm(self, message: str) -> bool:
        response = input(message).strip().lower()
        return response in ("y", "yes")

    # TODO: Improve confirm input handling
    # - handle empty input (e.g. just Enter)
    # - support more variations ("y", "yes", "n", "no")
    # - optionally reprompt user on invalid input
    # - consider case for default answer (e.g. Enter = yes/no)
    # - add validation loop instead of single input